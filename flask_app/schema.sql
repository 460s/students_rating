DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS t2u;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  repository TEXT NOT NULL
);

create table t2u
(
  id    INTEGER
    primary key
  autoincrement
    constraint t2u_tasks_task_fk
    references tasks (task)
      on update cascade
      on delete cascade
    constraint t2u_users_user_fk
    references users (user)
      on update cascade
      on delete cascade,
  grade INTEGER,
  task  INTEGER,
  user  INTEGER
);

create table task
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  description TEXT
);

create unique index tasks_name_uindex
  on task (name);

create unique index users_login_uindex
  on user (username);

INSERT INTO task (id, name, description) VALUES (1, 'Домашнее задание №1', 'TEXT');
INSERT INTO task (id, name, description) VALUES (2, 'Домашнее задание №2', 'TEXT');
INSERT INTO task (id, name, description) VALUES (3, 'Домашнее задание №3', 'TEXT');
INSERT INTO task (id, name, description) VALUES (4, 'Домашнее задание №4', 'TEXT');
INSERT INTO task (id, name, description) VALUES (5, 'Домашнее задание №5', 'TEXT');
INSERT INTO task (id, name, description) VALUES (6, 'Домашнее задание №6', 'TEXT');
INSERT INTO task (id, name, description) VALUES (7, 'Домашнее задание №7', 'TEXT');