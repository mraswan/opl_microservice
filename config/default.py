SERVICE_PORT = 8003

DATABASE_OPL = "db/opl_data.db"
SQL_SELECT_CATEGORY_SUB_CATEGORY = """
                                    select category.*, sub_category.* 
                                    from category inner join sub_category 
                                    on category.id = sub_category.category_id;
                                    """
SQL_ROW_COUNT = 20

SQL_SELECT_LESSON = """
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
                    {} 
                    ORDER BY lesson.published_timestamp DESC
                        limit {},{};"""

SQL_SELECT_LESSON_BY_ID = """
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
                             user.username as author_name
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


# SOLR_BASE = 'http://localhost:8983/solr'
# SOLR_COLLECTION_TALENT = '/dbAcc'
# SOLR_SELECT = '/select?'
# SOLR_DATA_IMPORT = '/dataimport?'
# SOLR_DATA_IMPORT_COMMAND = 'command='
# SOLR_DATA_IMPORT_ENTITY = '&entity='
# SOLR_DATA_IMPORT_CLEAN = '&clean='
