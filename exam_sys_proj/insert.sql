-- insert into homework_or_exam_pool (type, question, answer, courseName, difficultyLevel, isActive) VALUES ('选择题', '{
-- "main_content": "1+1=?",
-- "questions": ["等于1", "等于2", "等于3", "ABC都不对"],
-- "type": "选择题",
-- "shuffle": false,
-- "score": [5]
-- }', '{}', '数学', 1, true);
SET
@new_hoep_id = LAST_INSERT_ID();
insert into knowledge_points (kpID, kpName, subject)
VALUES (6661, '四则运算', '数学');
insert into knowledge_points (kpID, kpName, subject)
VALUES (6662, '三角函数', '数学');
insert into knowledge_points (kpName, subject)
VALUES (6663, '线性代数', '数学');
insert into knowledge_points (kpName, subject)
VALUES (6664, '微积分', '数学');
SET
@new_kp_id = LAST_INSERT_ID();
insert into hep_and_kp_mediater (hepID, kpID)
VALUES (@new_hoep_id, @new_kp_id);
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (666, 'Homura Akemi', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Homura Akemi
', 1, 'student@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (6666, '塔维尔·亚特·乌姆尔', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', '塔维尔·亚特·乌姆尔
', 2, 'teacher@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (66666, '犹格·索托斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', '犹格·索托斯', 3,
        'admin@test.com');
insert into teacher_course (userID, semester, courseName, isActive, class_, subject)
values (6666, '2022', '数学', 1, '1', '数学');
