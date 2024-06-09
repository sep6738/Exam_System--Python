-- insert into homework_or_exam_pool (type, question, answer, courseName, difficultyLevel, isActive) VALUES ('选择题', '{
-- "main_content": "1+1=?",
-- "questions": ["等于1", "等于2", "等于3", "ABC都不对"],
-- "type": "选择题",
-- "shuffle": false,
-- "score": [5]
-- }', '{}', '数学', 1, true);
SET
@new_hoep_id = LAST_INSERT_ID();
insert into knowledge_points (kpName, subject)
VALUES ('四则运算', '数学');
insert into knowledge_points (kpName, subject)
VALUES ('三角函数', '数学');
insert into knowledge_points (kpName, subject)
VALUES ('线性代数', '数学');
insert into knowledge_points (kpName, subject)
VALUES ('微积分', '数学');
-- SET
-- @new_kp_id = LAST_INSERT_ID();
-- insert into hep_and_kp_mediater (hepID, kpID)
-- VALUES (@new_hoep_id, @new_kp_id);
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (666, '晓美焰', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Homura Akemi
', 1, 'student@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (6666, '梅林·安布罗修斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Merlin Ambrosius
', 2, 'teacher@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (66666, '犹格·索托斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Yog-Sothoth', 3,
        'admin@test.com');
insert into teacher_course (userID, semester, courseName, isActive, class_, subject)
values (6666, '500', '数学', 1, '亚瑟王速成班', '数学');

insert into broadcast (content, duringTime, courseID)
values ('{
"title": "Weekly announcement",
"message": "Please be reminded of the upcoming exam schedule.",
"color": "red"
}', '2025-05-01 08:00:00', '数学');
insert into broadcast_show (userID, broadcastID, isActive)
values (6666, 1, 1);
