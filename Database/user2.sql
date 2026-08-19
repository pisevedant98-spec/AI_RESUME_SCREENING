USE ai_resume_screening;

INSERT INTO users (name, email, password, role)
VALUES (
    'Test Candidate',
    'candidate@gmail.com',
    'password123',
    'candidate'
);
SELECT * FROM users;