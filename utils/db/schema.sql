--comment
drop table if exists users;
drop table if exists articles;
drop table if exists modules;

create table users(
    id integer primary key autoincrement,
    username string not null,
    password string not null
);

create table articles(
    id integer primary key autoincrement,
    title string not null,
    text string not null,
    author string not null,
    publishtime text not null,
    text_type string default 'normal' not null,
    visiable int default 1 not null
);

create table modules(
    id integer primary key autoincrement,
    name string not null,
    url string not null,
    params string not null
);
