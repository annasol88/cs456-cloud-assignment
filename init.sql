CREATE DATABASE turbine;
CREATE USER 'webapp'@'%' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON turbine.* TO 'webapp'@'%';
USE turbine;