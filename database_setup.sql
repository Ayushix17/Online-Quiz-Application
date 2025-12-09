-- Create database
CREATE DATABASE IF NOT EXISTS online_quiz;

-- Use the database
USE online_quiz;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer CHAR(1) NOT NULL
);

-- Create quiz_results table
CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    time_taken_seconds INT NOT NULL,
    date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert sample questions
INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_answer) VALUES
('What is the capital of France?', 'Paris', 'London', 'Berlin', 'Madrid', 'A'),
('Which planet is known as the Red Planet?', 'Earth', 'Mars', 'Jupiter', 'Venus', 'B'),
('What is 2 + 2?', '3', '4', '5', '6', 'B'),
('Who wrote Romeo and Juliet?', 'Shakespeare', 'Dickens', 'Hemingway', 'Twain', 'A'),
('What is the largest ocean?', 'Atlantic', 'Indian', 'Arctic', 'Pacific', 'D');
