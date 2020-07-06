--sqlite3 db/opl_data.db

CREATE TABLE IF NOT EXISTS user_type(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT into user_type VALUES (1, 'super');
INSERT into user_type VALUES (2, 'power');
INSERT into user_type VALUES (3, 'user');

CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_type_id INTEGER NOT NULL
);

INSERT into user VALUES (1, "meghna","meghna",1);
INSERT into user VALUES (2, "shaurya","shaurya",2);
INSERT into user VALUES (3, "maneesh","maneesh",3);


CREATE TABLE IF NOT EXISTS lesson(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    youtube_url TEXT,
    git_url TEXT,
    published_timestamp TEXT,
    category_id INTEGER NOT NULL,
    sub_category_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS my_stuff(
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    completion_pct INTEGER
);

CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT into category VALUES (1,"Computer Science");
INSERT into category VALUES (2,"Science");
INSERT into category VALUES (3,"Math");


CREATE TABLE IF NOT EXISTS sub_category (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL
);

INSERT into sub_category VALUES (1,"C++",1);
INSERT into sub_category VALUES (2,"Java",1);
INSERT into sub_category VALUES (3,"Python",1);
INSERT into sub_category VALUES (4,"Node",1);
INSERT into sub_category VALUES (5,"Angular",1);

INSERT into sub_category VALUES (6,"Biology", 2);
INSERT into sub_category VALUES (8,"Chemistry", 2);
INSERT into sub_category VALUES (9,"Environmental Science", 2);

INSERT into sub_category VALUES (10,"Algebra", 3);
INSERT into sub_category VALUES (11,"Geometry", 3);
INSERT into sub_category VALUES (12,"Trigonometry", 3);
INSERT into sub_category VALUES (13,"Pre-Calculus", 3);
INSERT into sub_category VALUES (14,"Calculus", 3);
