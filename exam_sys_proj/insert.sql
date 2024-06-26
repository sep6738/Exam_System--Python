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
insert into knowledge_points (kpName, subject)
VALUES ('其他', '数学');

insert into users (userID, userName, passWord, name, roleID, email)
VALUES (666, '晓美焰', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Homura Akemi
', 1, 'student@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (6666, '梅林·安布罗修斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Merlin Ambrosius
', 2, 'teacher@test.com');
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (66666, '犹格·索托斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Yog-Sothoth', 3,
        'admin@test.com');
insert into teacher_course (courseID, userID, semester, courseName, class_, isActive, subject)
values (6666, 6666, '500', '亚瑟王速成班', 12345, 1, '数学');
insert into teacher_course (courseID, userID, semester, courseName, class_, isActive, subject)
values (6667, 6666, '500', '魔法少女速成班', 23456, 1, '数学');
insert into student_course (courseName, userID, semester, courseID, isDelete)
values ('数学', 666, '500', 6666, 0);
insert into broadcast (content, duringTime, courseID)
values ('{
"title": "Weekly announcement",
"message": "Please be reminded of the upcoming exam schedule.",
"color": "red"
}', '2025-05-01 08:00:00', '数学');

insert into broadcast_show (userID, broadcastID, isActive)
values (6666, 1, 1);
insert into users (userID, userName, passWord, name, roleID, email)
VALUES (777, '亚瑟·潘德拉贡', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Arthur Pendragon', 1,
        'arthur@camelot.com');

insert into users (userID, userName, passWord, name, roleID, email)
VALUES (778, '兰斯洛特·杜·拉克', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Lancelot du Lac', 1,
        'lancelot@camelot.com');

insert into users (userID, userName, passWord, name, roleID, email)
VALUES (779, '高文·奥克尼', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Gawain of Orkney', 1,
        'gawain@camelot.com');

insert into student_course (courseName, userID, semester, courseID, isDelete)
values ('亚瑟王速成班', 777, '500', 6666, 0);
insert into student_course (courseName, userID, semester, courseID, isDelete)
values ('亚瑟王速成班', 778, '500', 6666, 0);
insert into student_course (courseName, userID, semester, courseID, isDelete)
values ('亚瑟王速成班', 779, '500', 6666, 0);

-- INSERT INTO exam_sys.homework_or_exam_pool (hepID, type, question, answer, courseName, difficultyLevel, isActive)
-- VALUES (2, '选择题',
--         '{"type": "选择题", "score": [4.0], "shuffle": false, "questions": ["选择题1选项1", "选择题1选项2", "选择题1选项3", "选择题1选项4"], "main_content": "测试选择题1题干"}',
--         '["1"]', '数学', 5, true);
