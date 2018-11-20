DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  repository TEXT NOT NULL
);

create table t2u
(
  id INTEGER
    primary key
  autoincrement
    constraint task
    references tasks (task)
      on update cascade
      on delete cascade
    constraint user
    references users (user)
      on update cascade
      on delete cascade
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

