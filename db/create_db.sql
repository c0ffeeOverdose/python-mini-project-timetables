if EXISTS (SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'TimeTableDatabase') THEN
    DROP DATABASE `TimeTableDatabase`;
END IF;

CREATE DATABASE `TimeTableDatabase`;

USE `TimeTableDatabase`;

CREATE TABLE `Timetables` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Year` INT NOT NULL,
    `Term` INT NOT NULL,
    `Weekday` VARCHAR(16) NOT NULL,
    `Time` VARCHAR(16) NOT NULL,
    `Subject_Id` VARCHAR(16) NOT NULL,
    `Subject_Name` VARCHAR(128) NOT NULL,
    `Credit` VARCHAR(16) NOT NULL,
    `Classroom` VARCHAR(64) NOT NULL,
    `Section` INT NOT NULL,
    `Instructor_Name` VARCHAR(128) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
