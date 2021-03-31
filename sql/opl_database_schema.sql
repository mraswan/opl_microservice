--sqlite3 db/opl_data.db

CREATE TABLE IF NOT EXISTS user_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT into user_type VALUES (1, 'super');
INSERT into user_type VALUES (2, 'power');
INSERT into user_type VALUES (3, 'user');

CREATE TABLE IF NOT EXISTS user_new(
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    google_id TEXT,
    profile_pic TEXT,
    user_type_id INTEGER NOT NULL
);

Insert into user_new (id, user_type_id, email, name, display_name, user_type_id )
 SELECT id, user_type_id, username, name, display_name, user_type_id from user;

ALTER TABLE user RENAME TO user_old;
ALTER TABLE user_new RENAME TO user;

--# ------
--# PRAGMA foreign_keys=off;
--#
--# BEGIN TRANSACTION;
--#
--# ALTER TABLE app RENAME TO old_2_app;
--#
--# CREATE TABLE IF NOT EXISTS app (
--#                                 id integer PRIMARY KEY,
--#                                 app_id text NOT NULL,
--#                                 user text NOT NULL,
--#                                 name text NOT NULL,
--#                                 app_type text NOT NULL,
--#                                 queue text NOT NULL,
--#                                 start_time int NOT NULL,
--#                                 end_time int,
--#                                 state text,
--#                                 final_state text,
--#                                 tracking_url text,
--#                                 memory_seconds integer,
--#                                 vcore_seconds integer,
--#                                 preempted_mem_gb real,
--#                                 preempted_vcores integer,
--#                                 UNIQUE(app_id)
--#                             );
--#
--# INSERT INTO app (id,
--#                 app_id,
--#                 user,
--#                 name,
--#                 app_type,
--#                 queue,
--#                 start_time,
--#                 end_time,
--#                 state ,
--#                 final_state ,
--#                 tracking_url)
--# SELECT
--#               id,
--#               app_id,
--#               user,
--#               name,
--#               app_type,
--#               queue,
--#               start_time,
--#               end_time,
--#               state ,
--#               final_state ,
--#               tracking_url
--#             FROM old_2_app;
--#
--# COMMIT;
--#
--# PRAGMA foreign_keys=on;
--
--# -----


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

CREATE TABLE IF NOT EXISTS lesson_sub_category_xref(
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    sub_category_id INTEGER NOT NULL
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

#

#NEW VIDEOS!!!!
INSERT into lesson VALUES (5,
    "Python Data Types",
    "Learn Python Data Types using PyCharm! This tutorial is for beginners who have never typed Python code. We will learn how to work with strings, numbers, and booleans. We will also learn how to output the data on the screen using print statements.",
    "lOE-thp4YdE",
    "https://github.com/BiggBird/OPL",
    "1599936853",
    1,
    3,
    2
);

#Update Datatypes Video
UPDATE lesson SET name = "Python Data Types" WHERE id = 5;

#Alter user table by adding name and replace username with email
ALTER TABLE user ADD name TEXT;
ALTER TABLE user ADD display_name TEXT;

#Add users
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('tywongny@gmail.com', 'Tyler#04', 3, 'Tyler Wong', 'Tyler');

INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('nithinparthas@gmail.com', 'Nithin#13', 3, 'Nithin Parthasarathy', 'Nithin');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('ksonowal2468@gmail.com', 'Kunal#07', 3, 'Kunal Sonowal', 'Kunal');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('huangeric50@gmail.com', 'Eric#05', 3, 'Eric Huang', 'Eric');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('eltonmanchester@gmail.com', 'Elton#10', 3, 'Elton Manchester', 'Elton');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('sooon337733@gmail.com', 'Edward#04', 3, 'Edward Chen', 'Edward');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('epicdavidx@gmail.com', 'David#04', 3, 'David Xing', 'David');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('aaronchou2004@gmail.com', 'Aaron#04', 3, 'Aaron Chou', 'Aaron');
INSERT INTO user (username, password, user_type_id, name, display_name) VALUES ('adamkg30@gmail.com', 'Adam#06', 3, 'Adam Godina', 'Adam');

#BIOTECHNOLOGY VIDEOS
INSERT INTO sub_category (name, category_id) VALUES ("Biotechnology", 2);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Introduction to Bioremediation Part 1",
    "Today we will be learning about Biotechnology and Bioremediation with Tyler Wong. The impact of chemical pollutants, genomic programs, microbe usage in Bioremediation, and aerobic and anaerobic biodegradation are all topics covered in this video.",
    "2hIuENBhA94",
    "",
    "1603933727",
    2,
    18,
    4
);


INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Introduction to Bioremediation Part 2: Deepwater Horizon oil spill",
    "Today we will be learning more about Biotechnology and Bioremediation with Tyler Wong. We will be investigating the case study on the BP Deepwater oil spill in 2010, learning about the impacts it had on the ecosystem, marine life, and clean up crew. We will be specifically discussing containment booms, Corexit dispersant, and oil-eating microbes.",
    "C7WYJJ3zfWI",
    "",
    "1603933914",
    2,
    18,
    4
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Phytoremediation",
    "What is Phytoremediation and how does it happen on a molecular level? We will explore this topic today with Tyler Wong and discover the pros and cons of using this method.",
    "NsdeyweuIoo",
    "",
    "1603934257",
    2,
    18,
    4
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Ex Situ and In Situ",
    "Today we will explore the essential understanding of Ex Situ and In Situ with Tyler Wong. We will compare the differences and similarities between both methods.",
    "ajgVNBbGbYg",
    "",
    "1603934415",
    2,
    18,
    4
);

#Networking Videos
INSERT into sub_category (name, category_id) VALUES (
    "Networking",
    1
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Introduction to OPL",
    "I created this website, Online Peer Learning, which is a video hosting website where students can post and view videos that teach certain subjects, such as videos that teach mathematics, science, music, or computer science concepts. In this video, we will see all of the components of this website and how most websites are set up.",
    "E6kAyqsPbkk",
    "https://github.com/BiggBird/OPL",
    "1603934754",
    1,
    19,
    2
);

#foreign languages category
INSERT into category (name) VALUES ("Foreign Languages");
INSERT into sub_category (name, category_id) VALUES ("Korean", 5);
INSERT into sub_category (name, category_id) VALUES ("Spanish", 5);
INSERT into sub_category (name, category_id) VALUES ("French", 5);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Basics of Hangul",
    "Join Edward Chen and learn about how to read, write, and speak Korean! We will learn about Hangul, the writing system of the Korean language. The basics of Hangul covered today are how to pronounce constants and vowels. The list of the consonants and the vowels are slightly different from that of English but share the general idea of the English alphabet.",
    "mpSf4ptZfCc",
    "",
    "1604375980",
    5,
    20,
    9
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "How to Play Vibrato",
    "Many flute players utilize vibrato to make their playing sound more interesting, bringing depth to even the simplest of notes. In this video, Nithin Parthasarathy will introduce you to what vibrato is and a basic exercise to help learn it.",
    "vTn3o6AF-YM",
    "",
    "1604378212",
    4,
    17,
    5
);

INSERT into category (name) VALUES ("Art");
INSERT into sub_category (name, category_id) VALUES ("Pixel Art", 6);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Where to Start",
    "Aaron Chou teaches the basics of pixel art and where to start making beautiful pixel art. You could use this knowledge for any videos, games, or art you are creating!",
    "3MBRTCCvLwA",
    "",
    "1604380787",
    6,
    23,
    11
);

INSERT into sub_category (name, category_id) VALUES ("Painting", 6);
INSERT into sub_category (name, category_id) VALUES ("Digital Art", 6);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "How to Form Embouchure",
    "What is embouchure and how do I form my own embouchure? Today we will learn about those concepts with Kunal Sonowal. This tutorial is specifically for the trumpet, but it is also useful for people trying to form an embouchure for other brass instruments, such as the euphonium and trombone.",
    "85OWxuDvrf4",
    "",
    "1604417602",
    4,
    15,
    6
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Protein Synthesis",
    "How are proteins made, a nutrient essential to all living things? Eric Huang teaches about the process of protein synthesis and the exact steps in making functioning proteins, including the two main steps, transcription and translation.",
    "CR2C5kcYZUg",
    "",
    "1604537721",
    2,
    6,
    7
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Equation of a Line",
    "Learn how to find the equation of a line using 2 points or given a specific scenario with David Xing.",
    "Q0yRHEDRobI",
    "",
    "1606356697",
    3,
    10,
    10
);

INSERT into category (name) VALUES ("Games");
INSERT into sub_category (name, category_id) VALUES ("Chess", 7);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Rook Checkmates",
    "Details the strategy and method on checkmating with one rook and king and with two rooks.",
    "sa8TbxmfDac",
    "",
    "1608421304",
    7,
    26,
    12
);

INSERT into sub_category (name, category_id) VALUES ("Machine Learning", 1);
INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Intro to Machine Learning",
    "Welcome to the world of artificial intelligence! It may seem overwhelming at first, but don't worry, because today we will talk about the simple basics and essential knowledge of machine learning! Machine learning is an application of AI where computer systems are able to function and learn through experience without being explicitly programmed. We will be using a website called Kaggle.com, a data science website owned by Google, to grasp the basics of machine learning and start coding! Knowing a little Python would be helpful.",
    "Awh6RjjgKjw",
    "",
    "1611091677",
    1,
    27,
    2
);

INSERT into sub_category (name, category_id) VALUES ("Editing", 6);
INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "How to Remove Static Noise Using Audacity",
    "Learn how to remove the static/fuzzy sound when recording audio using Audacity.",
    "aK_0upDDEks",
    "",
    "1611130251",
    6,
    28,
    11
);

INSERT into sub_category (name, category_id) VALUES ("Music Theory", 4);
INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "How to Read Music",
    "Learn to read music for beginners with Eric Huang.",
    "Af1vIftmbVA",
    "",
    "1611447045",
    4,
    29,
    7
);
UPDATE lesson SET published_timestamp = 1611447045 WHERE id = 20;

DELETE FROM lesson WHERE id in (1, 2, 3, 4);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Buzzing",
    "In the last video, we talked about how to form your embouchure, and now the next step is to start buzzing on your trumpet mouthpiece while keeping your embouchure in mind.",
    "8EA70OkrTOU",
    "",
    "1604417602",
    4,
    15,
    6
);

INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Common Music Notation",
    "David Xing highlights common music notation for beginners, including the basic principles of music.",
    "oQxKa2acSaU",
    "",
    "1612742188",
    4,
    29,
    10
);


INSERT into lesson (name,
    description,
    youtube_url,
    git_url,
    published_timestamp,
    category_id,
    sub_category_id,
    author_id)
    VALUES (
    "Reading Beyond the Notes",
    "Learn to read music notes more in-depth with Nithin Parthasarathy by reading beyond what is written down.",
    "MEjIAazIZzk",
    "",
    "1617053076",
    4,
    29,
    5
);

