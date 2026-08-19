CREATE DATABASE ai_resume_screening;
USE ai_resume_screening;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('candidate','hr') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    phone VARCHAR(15),
    education VARCHAR(200),
    experience VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE hr_admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    department VARCHAR(100),
    designation VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    required_skills TEXT,
    experience_required VARCHAR(100),
    education_required VARCHAR(100),
    status ENUM('Open','Closed') DEFAULT 'Open'
);

CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    file_path VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
);

CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    job_id INT,
    status ENUM(
        'Applied',
        'Under Review',
        'AI Screened',
        'Shortlisted',
        'Interview',
        'Selected',
        'Rejected'
    ) DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);