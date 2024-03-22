CREATE DATABASE IF NOT EXISTS turbine_monitor;
CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY '123' REQUIRE SSL;
CREATE USER IF NOT EXISTS 'functionapp'@'%' IDENTIFIED BY '456' REQUIRE SSL;
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'webapp'@'%';
GRANT ALL PRIVILEGES ON turbine_monitor.* TO 'functionapp'@'%';
USE turbine_monitor;