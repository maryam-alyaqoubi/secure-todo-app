CREATE DATABASE IF NOT EXISTS secure_todo_db;
CREATE USER IF NOT EXISTS 'todo_user'@'%' IDENTIFIED BY 'todo_pass';
GRANT ALL PRIVILEGES ON secure_todo_db.* TO 'todo_user'@'%';
FLUSH PRIVILEGES;
