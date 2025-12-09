-- إنشاء قاعدة بيانات
CREATE DATABASE secure_todo_db;

-- إنشاء مستخدم لتطبيق Flask
CREATE USER 'todo_user'@'localhost' IDENTIFIED BY '123';

-- إعطاء صلاحيات كاملة للمستخدم على قاعدة البيانات
GRANT ALL PRIVILEGES ON secure_todo_db.* TO 'todo_user'@'localhost';

-- تطبيق الصلاحيات
FLUSH PRIVILEGES;
