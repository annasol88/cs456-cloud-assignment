CREATE DATABASE IF NOT EXISTS turbine_monitor;
CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '<replace me>';
CREATE USER IF NOT EXISTS 'funcapp'@'%' IDENTIFIED BY '<replace me>';
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'webapp'@'%';
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'funcapp'@'%';
USE turbine_monitor;