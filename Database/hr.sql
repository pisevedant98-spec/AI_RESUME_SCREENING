USE ai_resume_screening;

SELECT id, name, email, password, role
FROM users
WHERE email = 'hr@gmail.com';