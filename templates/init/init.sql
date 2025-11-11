CREATE DATABASE IF NOT EXISTS flaskdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE flaskdb;

CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50)
);

INSERT INTO members (name, email, city) VALUES
('홍길동', 'hong@example.com', '서울'),
('이순신', 'lee@example.com', '부산');