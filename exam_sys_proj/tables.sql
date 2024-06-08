create table broadcast
(
    broadcastID int auto_increment
        primary key,
    content     json         null,
    duringTime  varchar(255) null,
    courseID    varchar(255) null
);

create table homework_or_exam_pool
(
    hepID           int auto_increment
        primary key,
    type            varchar(255) null,
    question        json         null,
    answer          json         null,
    courseName      varchar(255) null,
    difficultyLevel int          null,
    isActive        bit          null
);

create table exam_pool
(
    epID           int auto_increment
        primary key,
    examID         int          null,
    questionID     int          null,
    questionNumber int          null,
    title          varchar(255) null,
    constraint exam_pool_homework_or_exam_pool_hepID_fk
        foreign key (questionID) references homework_or_exam_pool (hepID)
            on update cascade on delete cascade
);

create index exam_pool_examID_index
    on exam_pool (examID);

create index homework_or_exam_pool_hepID_index
    on homework_or_exam_pool (hepID);

create table knowledge_points
(
    kpID    int auto_increment
        primary key,
    kpName  varchar(255) null,
    subject varchar(255) null,
    constraint kpname_u
        unique (kpName)
);

create table hep_and_kp_mediater
(
    mediaterID int auto_increment
        primary key,
    hepID      int          null,
    kpName     varchar(255) null,
    constraint hep_and_kp_mediater_homework_or_exam_pool_hepID_fk
        foreign key (hepID) references homework_or_exam_pool (hepID)
            on update cascade on delete cascade,
    constraint hep_and_kp_mediater_knowledge_points_kpName_fk
        foreign key (kpName) references knowledge_points (kpName)
            on update cascade on delete cascade
);

create index hep_and_kp_mediater_kpName_index
    on hep_and_kp_mediater (kpName);

create table registration_code
(
    email            varchar(255) not null
        primary key,
    verificationCode varchar(6)   null,
    expirationDate   datetime     null
);

create table role
(
    roleID   int auto_increment
        primary key,
    roleName varchar(255) null
);

create table users
(
    userID   int auto_increment
        primary key,
    userName varchar(255) null,
    passWord varchar(255) null,
    name     varchar(255) null,
    roleID   int          null,
    createAt datetime     null,
    updateAt datetime     null,
    email    varchar(255) not null,
    constraint email
        unique (email)
);

create table broadcast_show
(
    broadcastShowID int auto_increment
        primary key,
    userID          int null,
    broadcastID     int null,
    isActive        bit null,
    constraint broadcast_show_broadcast_broadcastID_fk
        foreign key (broadcastID) references broadcast (broadcastID)
            on update cascade on delete cascade,
    constraint broadcast_show_users_userID_fk
        foreign key (userID) references users (userID)
            on update cascade on delete cascade
);

create table teacher_course
(
    courseID   int auto_increment
        primary key,
    userID     int          null,
    semester   varchar(255) null,
    time       varchar(255) null,
    courseName varchar(255) null,
    isActive   bit          null,
    class_     varchar(6)   not null,
    subject    varchar(255) null,
    constraint teacher_course_users_userID_fk
        foreign key (userID) references users (userID)
);

create table b_and_tc_mediater
(
    mediaterID  int auto_increment
        primary key,
    broadcastID int null,
    courseID    int null,
    constraint b_and_tc_mediater_broadcast_broadcastID_fk
        foreign key (broadcastID) references broadcast (broadcastID)
            on update cascade on delete cascade,
    constraint b_and_tc_mediater_teacher_course_courseID_fk
        foreign key (courseID) references teacher_course (courseID)
            on update cascade on delete cascade
);

create table homework_or_exam
(
    heID               int auto_increment
        primary key,
    courseID           int          null,
    duringTime         varchar(255) null,
    homeworkExamPoolID int          null,
    result             json         null,
    constraint homework_or_exam_homework_or_exam_pool_hepID_fk
        foreign key (homeworkExamPoolID) references homework_or_exam_pool (hepID)
            on update cascade on delete cascade,
    constraint homework_or_exam_teacher_course_courseID_fk
        foreign key (courseID) references teacher_course (courseID)
            on update cascade on delete cascade
);

create table student_course
(
    scID       int auto_increment
        primary key,
    courseName varchar(255)  null,
    userID     int           null,
    semester   varchar(255)  null,
    time       varchar(255)  null,
    grade      decimal(5, 2) null,
    courseID   int           null,
    isDelete   bit           null,
    constraint student_course_teacher_course_courseID_fk
        foreign key (courseID) references teacher_course (courseID)
            on update cascade on delete cascade,
    constraint student_course_users_userID_fk
        foreign key (userID) references users (userID)
            on update cascade on delete cascade
);

create table student_hand_in
(
    studentHandInID int auto_increment
        primary key,
    userID          int           null,
    homeworkExamID  int           null,
    content         json          null,
    upTime          varchar(255)  null,
    score           decimal(5, 2) null,
    teacherComment  varchar(255)  null,
    resultDetails   json          null,
    constraint student_hand_in_homework_or_exam_heID_fk
        foreign key (homeworkExamID) references homework_or_exam (heID)
            on update cascade on delete cascade,
    constraint student_hand_in_users_userID_fk
        foreign key (userID) references users (userID)
            on update cascade on delete cascade
);

create index users_role_roleID_fk
    on users (roleID);

