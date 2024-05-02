from dataclasses import dataclass
from typing import Union, Literal, Optional, TypeVar, Sequence, Generator, Any

from mysql import connector
from mysql.connector.abstracts import  MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection

from env import ENV

T = TypeVar("T")
Result = Union[tuple[Literal[True], T], tuple[Literal[False], str]]

@dataclass(init=False, slots=True)
class Timetable:
    id: Optional[int] = None
    year: int = 0
    term: int = 0
    classWeekday: str = ""
    time: str = ""
    subjectId: str = ""
    subjectName: str = ""
    subjectCredit: str = ""
    classroom: str = ""
    classSection: int = 0
    instructor: str = ""

    def __init__(self, *args) -> None:
        for key, val in zip(self.__slots__, args):
            setattr(self, key, val)

    def __iter__(self) -> Generator[Any, Any, None]:
        for key in self.__slots__:
            yield getattr(self, key)

class Database:
    global Result, Timetable

    connection: PooledMySQLConnection | MySQLConnectionAbstract
    cursor: MySQLCursorAbstract

    tableName: str
    columns = ("id", "Year", "Term", "Weekday", "Time", "Subject_Id", "Subject_Name", "Credit", "Classroom", "Section", "Instructor_Name")
    columns_str = ", ".join(columns)
    values_format_str = ", ".join(["%s" for _ in range(len(columns))])
    values_eq_format_str = ", ".join([f"{name}=%s" for name in columns])
    values_eq_format_noid_str = ", ".join([f"{name}=%s" for name in columns[1:]])

    def __init__(self) -> None:
        self.connection = connector.connect(
            host = ENV["HOSTNAME"] or '127.0.0.1',
            port = 3306,
            username = ENV["USERNAME"],
            password = ENV["PASSWORD"],
            database = ENV["DATABASE"] or 'TimeTableDatabase'
        )

        self.tableName = ENV["TABLENAME"]
        self.cursor = self.connection.cursor()

    def get(self) -> Result[list[Timetable]]:
        try:
            data: list[Timetable] = []
            self.cursor.execute(f"SELECT {self.columns_str} FROM {self.tableName}")
            result = self.cursor.fetchall()
            if type(result) is list:
                for row in result:
                    if type(row) is tuple:
                        data.append(Timetable(*row))
        except Exception as err:
            return (False, str(err))

        data.sort(key=lambda x: x.year + (x.term * 10))

        return (True, data)

    def update(self, data: Sequence[Timetable], old_data: Sequence[Timetable]) -> Result[bool]:
        try:
            new_data = []
            update_data = []
            for obj in data:
                if obj.id is None:
                    new_data.append(tuple(obj))
                else:
                    for old_obj in old_data:
                        if obj.id == old_obj.id:
                            if obj != old_obj:
                                rec = list(obj)
                                rec.append(rec[0])
                                rec.pop(0)
                                update_data.append(tuple(rec))
                            break

            no_removed: list[str] = []
            for old_obj in old_data:
                if old_obj is not None:
                    for obj in data:
                        if old_obj.id == obj.id:
                            break
                    else:
                        no_removed.append(str(old_obj.id))

            isupdate = False

            if len(no_removed) > 0:
                isupdate = True
                self.cursor.execute(f"DELETE FROM {self.tableName} WHERE id IN ({', '.join(no_removed)})")
            if len(new_data) > 0:
                isupdate = True
                self.cursor.executemany(f"INSERT INTO {self.tableName} ({self.columns_str}) VALUES ({self.values_format_str})", new_data)
            if len(update_data) > 0:
                isupdate = True
                self.cursor.executemany(f"UPDATE {self.tableName} SET {self.values_eq_format_noid_str} WHERE id = %s", update_data)
            self.connection.commit()
        except Exception as err:
            self.connection.rollback()
            return (False, str(err))

        return (True, isupdate)

    def close(self):
        self.cursor.close()
        self.connection.close()

db = Database()
