CREATE USER 'timetable'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON `TimeTableDatabase`.* TO 'timetable'@'%';
FLUSH PRIVILEGES;
