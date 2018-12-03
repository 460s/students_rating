DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS t2u;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  repository TEXT NOT NULL,
  is_admin INTEGER
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
  grade REAL,
  task  INTEGER,
  user  INTEGER
);

create table task
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT,
  description TEXT,
  pass_from   INTEGER,
  pass_to     INTEGER
);

create unique index tasks_name_uindex
  on task (name);

create unique index users_login_uindex
  on user (username);

INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (1, 'Домашнее задание №1', 'TEXT', 1542805200, 1543222800);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (2, 'Домашнее задание №2', 'TEXT', 1543237200, 1543395600);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (3, 'Домашнее задание №3', 'TEXT', 1543410000, 1543827600);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (4, 'Домашнее задание №4', 'TEXT', 1543842000, 1544000400);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (5, 'Домашнее задание №5', 'TEXT', 1544014800, 1544432400);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (6, 'Домашнее задание №6', 'TEXT', 1544446800, 1544605200);
INSERT INTO task (id, name, description, pass_from, pass_to) VALUES (7, 'Домашнее задание №7', 'TEXT', 1544619600, 1545037200);