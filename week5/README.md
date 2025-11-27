# Week 5 
## Task 2 : Create database and table in your MySQL server
```
mysql> CREATE DATABASE IF NOT EXISTS website
    -> USE website;

mysql> CREATE TABLE member(
    -> id INT UNSIGNED AUTO_INCREMENT,
    -> name VARCHAR(255) NOT NULL,
    -> email VARCHAR(255) NOT NULL,
    -> password VARCHAR(255) NOT NULL,
    -> follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    -> time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -> PRIMARY KEY (id)
    -> );
```
![Create a new database named website and a new table named member.](./images/task2.png)

## Task 3 : SQL CRUD
### 3-1
```
mysql> INSERT INTO member (name, email, password, follower_count)
    -> VALUES
    -> ('test', 'test@test.com', 'test', 3),
    -> ('Rachel', 'Rachel@test.com', 'pw1', 4),
    -> ('Monica', 'Monica@test.com', 'pw2', 7),
    -> ('Chandler', 'Chandler@test.com', 'pw3', 2),
    -> ('Ross', 'Ross@test.com', 'pw4', 1);
```
![Insert 5 rows.](./images/task3-1.png)

### 3-2
```
mysql> SELECT * FROM member;
```
![SELECT all rows from the member table.](./images/task3-2.png)

### 3-3
```
mysql> SELECT * FROM member ORDER BY time DESC;
```
![SELECT all rows from the member table, in descending order of time.](./images/task3-3.png)

### 3-4
```
mysql> SELECT * 
    -> FROM member
    -> ORDER BY time DESC
    -> LIMIT 1, 3;
```
![SELECT total 3 rows, second to fourth, in descending order of time.](./images/task3-4.png)

### 3-5
```
mysql> SELECT * 
    -> FROM member
    -> WHERE email = 'test@test.com';
```
![SELECT rows where email equals to test@test.com](./images/task3-5.png)

### 3-6
```
mysql> SELECT *
    -> FROM member
    -> WHERE name LIKE '%es%';
```
![SELECT rows where name includes the 'es' keyword.](./images/task3-6.png)

### 3-7
```
mysql> SELECT *
    -> FROM member
    -> WHERE email = 'test@test.com'
    -> AND password = 'test';
```
![SELECT rows where email equals to test@test.com and password equals to test.](./images/task3-7.png)

### 3-8
```
mysql> UPDATE member
    -> SET name = 'test2'
    -> WHERE email = 'test@test.com';
```
![UPDATE data in name column to test2 where email equals to test@test.com.](./images/task3-8.png)

## Task 4 : SQL Aggregation Functions
### 4-1
```
mysql> SELECT COUNT(*) AS total_members
    -> FROM member;
```
![SELECT how many rows from the member table.](./images/task4-1.png)

### 4-2
```
mysql> SELECT SUM(follower_count) AS sum_followers
    -> FROM member;
```
![SELECT the sum of follower count of all the rows from the member table.](./images/task4-2.png)

### 4-3
```
mysql> SELECT AVG(follower_count) AS avg_followers
    -> FROM member
```
![SELECT the average of follower count of all the rows from the member table.](./images/task4-3.png)

### 4-4
```
mysql> SELECT AVG(follower_count) AS avg_followers_of_top2
    -> FROM (
    -> SELECT follower_count
    -> FROM member
    -> ORDER BY follower_count DESC
    -> LIMIT 2
    -> ) AS a;
```
![SELECT the average of follower count of the first 2 rows, in descending order of
follower count, from the member table.](./images/task4-4.png)

## Task 5 : SQL JOIN
### 5-1
```
mysql> CREATE TABLE message(
    -> id INT UNSIGNED AUTO_INCREMENT,
    -> member_id INT UNSIGNED NOT NULL,
    -> content TEXT(65535) NOT NULL,
    -> like_count INT UNSIGNED NOT NULL DEFAULT 0,
    -> time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -> PRIMARY KEY (id),
    -> FOREIGN KEY (member_id) REFERENCES member(id)
    -> );
```
![Create a new table named message, in the website database.](./images/task5-1.png)

### 5-2
```
mysql> SELECT 
    -> m.id,
    -> m.content,
    -> m.like_count,
    -> m.time,
    -> mem.name  AS sender_name,
    -> mem.email AS sender_email
    -> FROM message AS m
    -> JOIN member AS mem 
    ->  ON m.member_id = mem.id;
```
![SELECT all messages, including sender names.](./images/task5-2.png)

### 5-3
```
mysql> SELECT
    -> m.id,
    -> m.content,
    -> m.like_count,
    -> m.time
    -> FROM message AS m
    -> JOIN member AS mem
    -> ON m.member_id  = mem.id
    -> WHERE mem.email = 'test@test.com';
```
![SELECT all messages, including sender names, where sender email equals to test@test.com.](./images/task5-3.png)

### 5-4
```
mysql> SELECT 
    -> AVG(m.like_count) AS avg_likes
    -> FROM message AS m
    -> JOIN member AS mem
    -> ON m.member_id = mem.id
    -> WHERE mem.email = 'test@test.com';
```
![get the average like count of messages where sender email equals to test@test.com .](./images/task5-4.png)

### 5-5
```
mysql> SELECT
    -> mem.email,
    -> AVG(m.like_count) AS avg_likes
    -> FROM message AS m
    -> JOIN member AS mem
    -> ON m.member_id  = mem.id
    -> GROUP BY mem.email;
```
![get the average like count of messages GROUP BY sender email.](./images/task5-5.png)
