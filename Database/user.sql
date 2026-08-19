USE ai_resume_screening;

INSERT INTO users (name, email, password, role)
VALUES (
    'Test HR',
    'hr@gmail.com',
    'password123',
    'hr'
);


SELECT * FROM users;