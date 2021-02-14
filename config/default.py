SERVICE_PORT = 8003

GOOGLE_CALLBACK_URL="https://www.oplearning.org"

GOOGLE_DISCOVERY_URL=GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

DATABASE_OPL = "db/opl_data.db"
SQL_SELECT_CATEGORY_SUB_CATEGORY = """
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
                                    """

# SQL_SELECT_CATEGORY_SUB_CATEGORY = """
#                                     select category.*, sub_category.*
#                                     from category inner join sub_category
#                                     on category.id = sub_category.category_id
#                                     order by category.name asc, sub_category.name asc;
#                                     """

SQL_ROW_COUNT = 50

SQL_SELECT_LESSON = """
                    SELECT lesson.id, lesson.name, lesson.description, lesson.youtube_url, lesson.git_url, lesson.published_timestamp,
                             category.id as category_id, category.name as category_name, sub_category.id as sub_category_id, sub_category.name as sub_category_name,
                             user.display_name as author_name
                    FROM category
                    INNER JOIN sub_category
                        ON category.id = sub_category.category_id
                    INNER JOIN lesson
                        ON sub_category.id = lesson.sub_category_id
                    INNER JOIN user
                        ON lesson.author_id = user.id 
                    {} 
                    ORDER BY lesson.published_timestamp DESC
                        limit {},{};"""

SQL_SELECT_LESSON_BY_ID = """
                    SELECT lesson.id, lesson.name, lesson.description, lesson.youtube_url, lesson.git_url, lesson.published_timestamp,
                             category.id as category_id, category.name as category_name, sub_category.id as sub_category_id, sub_category.name as sub_category_name,
                             user.display_name as author_name
                    FROM category
                    INNER JOIN sub_category
                        ON category.id = sub_category.category_id
                    INNER JOIN lesson
                        ON sub_category.id = lesson.sub_category_id
                    INNER JOIN user
                        ON lesson.author_id = user.id 
                    WHERE lesson.id = {};
                    """

SQL_SELECT_LESSON_COUNT = """
                    SELECT count(*) as count
                    FROM category
                    INNER JOIN sub_category
                        ON category.id = sub_category.category_id
                    INNER JOIN lesson
                        ON sub_category.id = lesson.sub_category_id
                    INNER JOIN user
                        ON lesson.author_id = user.id;"""

SQL_SELECT_FIND_LESSON = """
                    SELECT lesson.id, lesson.name, lesson.description, lesson.youtube_url, lesson.git_url, lesson.published_timestamp,
                             category.id as category_id, category.name as category_name, sub_category.id as sub_category_id, sub_category.name as sub_category_name,
                             user.display_name as author_name
                    FROM category
                    INNER JOIN sub_category
                        ON category.id = sub_category.category_id
                    INNER JOIN lesson
                        ON sub_category.id = lesson.sub_category_id
                    INNER JOIN user
                        ON lesson.author_id = user.id 
                    WHERE 
                        lesson.name like '%{}%' or
                        lesson.description like '%{}%' or
                        category.name like '%{}%' or
                        sub_category.name like '%{}%'
                    ORDER BY lesson.published_timestamp DESC
                        limit {},{};"""


SQL_SELECT_USER_BY_GOOGLE_ID = """
                    SELECT id, email, name, display_name, google_id, profile_pic, user_type_id 
                    FROM user WHERE google_id = ?;
                    """
SQL_SELECT_USER_BY_ID = """
                    SELECT id, email, name, display_name, google_id, profile_pic, user_type_id 
                    FROM user WHERE id = ?;
                    """

SQL_SELECT_USER_BY_EMAIL = """
                    SELECT id, email, name, display_name, google_id, profile_pic, user_type_id 
                    FROM user WHERE email = ?;
                    """

SQL_UPDATE_GOOGLE_INFO = """
                    UPDATE user 
                    SET 
                    name = ?,
                    display_name = ?, 
                    google_id = ?,
                    profile_pic = ?
                    WHERE email = ?;
                    """

SQL_INSERT_USER = """
                    INSERT INTO user 
                            (email, name, display_name, google_id, profile_pic, user_type_id) 
                    VALUES 
                            (?, ?, ?, ?, ?, ?);
                    """

# Insert into user_new (id, user_type_id,  )
#         from SELECT id, user_type_id, username, name, display_name from user;