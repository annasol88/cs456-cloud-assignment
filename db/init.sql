CREATE DATABASE turbine_monitor;
CREATE USER 'webapp'@'%' IDENTIFIED BY '123';
CREATE USER 'functionapp'@'%' IDENTIFIED BY '456';
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'webapp'@'%';
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'functionapp'@'%';
USE turbine_monitor;