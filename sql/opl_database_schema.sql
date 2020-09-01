--sqlite3 db/opl_data.db

CREATE TABLE IF NOT EXISTS user_type (
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
INSERT into sub_category VALUES (7,"Physics", 2);
INSERT into sub_category VALUES (8,"Chemistry", 2);
INSERT into sub_category VALUES (9,"Environmental Science", 2);

INSERT into sub_category VALUES (10,"Algebra", 3);
INSERT into sub_category VALUES (11,"Geometry", 3);
INSERT into sub_category VALUES (12,"Trigonometry", 3);
INSERT into sub_category VALUES (13,"Pre-Calculus", 3);
INSERT into sub_category VALUES (14,"Calculus", 3);


INSERT into lesson VALUES (1,
    "Meiosis by Amoeba Sisters",
    "Join the Amoeba Sisters as they explore the meiosis stages with vocabulary including chromosomes, centromeres, centrioles, spindle fibers, and crossing over. ",
    "VzDMG7ke69g",
    "https://github.com/BiggBird/OPL",
    "1594875503",
    2,
    6,
    2
);

INSERT into lesson VALUES (2,
    "Intro to Cell Signaling by Amoeba Sisters",
    "Explore cell signaling with the Amoeba Sisters! This introductory video describes vocabulary such as ligand and receptor. It includes the stages of cell signaling (reception, transduction, and response) and different types of signaling including autocrine, paracrine, and endocrine. ",
    "-dbRterutHY",
    "https://github.com/BiggBird/OPL",
    "1594875503",
    2,
    6,
    2
);

INSERT into lesson VALUES (3,
    "The Cell Cycle (and cancer) by Amoeba Sisters",
    "Explore the cell cycle with the Amoeba Sisters and an important example of when it is not controlled: cancer. ",
    "QVCjdNxJreE",
    "https://github.com/BiggBird/OPL",
    "1594875503",
    2,
    6,
    2
);

INSERT into lesson VALUES (4,
    "Mitosis: The Amazing Cell Process that Uses Division to Multiply! by Amoeba Sisters",
    "The Amoeba Sisters walk you through the reason for mitosis with mnemonics for prophase, metaphase, anaphase, and telophase. ",
    "f-ldPgEfAHI",
    "https://github.com/BiggBird/OPL",
    "1594875503",
    2,
    6,
    2
);


SELECT * FROM category
INNER JOIN sub_category
ON category.id = sub_category.category_id;


SELECT lesson.id, lesson.name, description, youtube_url, git_url, published_timestamp,
                 category.id, category.name, sub_category.id, sub_category.name,
                 user.username as author_name FROM category
INNER JOIN sub_category
    ON category.id = sub_category.category_id
INNER JOIN lesson
    ON sub_category.id = lesson.sub_category_id
INNER JOIN user
    ON lesson.author_id = user.id;


SELECT lesson.id, lesson.name, lesson.description, lesson.youtube_url, lesson.git_url, lesson.published_timestamp,
                             category.id as category_id, category.name as category_name, sub_category.id as sub_category_id, sub_category.name as sub_category_name,
                             user.username as author_name
                    FROM category
                    INNER JOIN sub_category
                        ON category.id = sub_category.category_id
                    INNER JOIN lesson
                        ON sub_category.id = lesson.sub_category_id
                    INNER JOIN user
                        ON lesson.author_id = user.id
                    WHERE
                        lesson.name like '%explore%' or
                        lesson.description like '%explore%' or
                        category.name like '%explore%' or
                        sub_category.name like '%explore%';


#inserting music into db
INSERT into category VALUES (4,"Music");
INSERT into sub_category VALUES (15,"Trumpet", 4);
INSERT into sub_category VALUES (16,"Trombone", 4);
INSERT into sub_category VALUES (17,"Flute", 4);
