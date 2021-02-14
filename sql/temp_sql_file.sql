SELECT category.id as category_id, category.name as category_name,count(*) as category_count
                    FROM category
                    INNER JOIN lesson
                    ON category.id = lesson.category_id
                    GROUP BY category.id;


SELECT sub_category.id as sub_category_id, sub_category.name as sub_category_name, count(sub_category.id) as sub_category_count,
       category.id as category_id, category.name as category_name
                    FROM sub_category
                    INNER JOIN lesson
                    ON sub_category.id = lesson.sub_category_id
                    INNER JOIN category
                    ON category.id = sub_category.category_id
                    GROUP BY sub_category.id;

INSERT into lesson VALUES (6,
    "Other ... Python Data Types",
    "Learn Python Data Types using PyCharm! This tutorial is for beginners who have never typed Python code. We will learn how to work with strings, numbers, and booleans. We will also learn how to output the data on the screen using print statements.",
    "lOE-thp4YdE",
    "https://github.com/BiggBird/OPL",
    "1599936853",
    1,
    2,
    2
);

select category.*, sub_category.*, sub_cat_grp.sub_category_count
        from category inner join sub_category
        on category.id = sub_category.category_id
        LEFT OUTER JOIN
        (SELECT sub_cat.id as sub_category_id,
                count(sub_cat.id) as sub_category_count
            FROM sub_category sub_cat
            INNER JOIN lesson
            ON sub_cat.id = lesson.sub_category_id
            GROUP BY sub_cat.id) sub_cat_grp
        on sub_cat_grp.sub_category_id = sub_category.id
        order by category.name asc, sub_category.name asc;

select id, sub_category_id from lesson;

Insert into user_new (id, user_type_id, email, name, display_name, user_type_id )
        from SELECT id, user_type_id, username, name, display_name, user_type_id from user;