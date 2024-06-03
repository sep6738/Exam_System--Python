insert into homework_or_exam_pool (hepID, type, question, answer, courseName, difficultyLevel, isActive) VALUES (1, '选择题', '{
"main_content": "1+1=?",
"questions": ["等于1", "等于2", "等于3", "ABC都不对"],
"type": "选择题",
"shuffle": "False",
"score": [5]
}', '{}', '数学', 1, true);
insert into knowledge_points (kpID, kpName, subject) VALUES (1, '四则运算', '数学');
insert into hep_and_kp_mediater (hepID, kpID) VALUES (1, 1);
insert into users (userName, passWord, name, roleID, email)
VALUES ('Homura Akemi', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', 'Homura Akemi
', 1, 'student@test.com');
insert into users (userName, passWord, name, roleID, email)
VALUES ('塔维尔·亚特·乌姆尔', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', '塔维尔·亚特·乌姆尔
', 2, 'teacher@test.com');
insert into users (userName, passWord, name, roleID, email)
VALUES ('犹格·索托斯', '$2b$08$C2pRyZ4v8WHy1BYml6kw1enOkUMvjCbbdrULL6ZThC92ej4TttYzG', '犹格·索托斯', 3,
        'admin@test.com');
