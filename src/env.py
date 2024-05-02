from typing import TypedDict
from pathlib import Path
from dotenv import dotenv_values

class ENVTyped(TypedDict):
    HOSTNAME: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DATABASE: str
    TABLENAME: str
    DARKMODE: int

dotenv_path = Path(__file__).resolve().parents[1].joinpath(".ENV")
values = dotenv_values(dotenv_path)

ENV = ENVTyped(
    HOSTNAME=(values["HOSTNAME"] or "127.0.0.1"),
    PORT=(int(values["PORT"] or 3306)),
    USERNAME=(values["USERNAME"] or "root"),
    PASSWORD=(values["PASSWORD"] or ""),
    DATABASE=(values["DATABASE"] or "TimeTableDatabase"),
    TABLENAME=(values["TABLENAME"] or "Timetables"),
    DARKMODE=(int(values["DARKMODE"] or 0)),
)
