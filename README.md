
#  Python-Final Project: Timetables

This repository is a Mini Python project that I studied in university. which has been assigned to The program requires CRUD (Create, Read, Update, and Delete) and GUI (Graphical User Interface).

- Programming Language : Python
- CRUD : MySQL
- GUI : PyQt6

## About development

- OS : Linux
- Python : 3.11.8
  - mysql-connector-python : 8.3.0
  - PyQt6 : 6.7.0
  - PyQt6-Qt6 : 6.7.0
  - PyQt6-sip : 13.6.0
  - python-dotenv : 1.0.1

## Config file

.ENV

```
HOSTNAME=127.0.0.1
PORT=3306
USERNAME=timetable
PASSWORD=
DATABASE=TimeTableDatabase
TABLENAME=Timetables
DARKMODE=0
```

## Setup

### Database

```sh
mysql < ./db/create_db.sql
mysql < ./db/create_user.sql
```

### Python setup

```sh
python3.11 -m venv env
source ./env/bin/activate
pip install -r ./requirements.txt
```

### Run

```sh
python src/main.py
```
