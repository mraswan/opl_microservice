SERVICE_PORT = 8003

DATABASE_OPL = "db/opl_data.db"
SQL_SELECT_CATEGORY_SUB_CATEGORY = """
                                    select category.*, sub_category.* 
                                    from category inner join sub_category 
                                    on category.id = sub_category.category_id;
                                    """


# SOLR_BASE = 'http://localhost:8983/solr'
# SOLR_COLLECTION_TALENT = '/dbAcc'
# SOLR_SELECT = '/select?'
# SOLR_DATA_IMPORT = '/dataimport?'
# SOLR_DATA_IMPORT_COMMAND = 'command='
# SOLR_DATA_IMPORT_ENTITY = '&entity='
# SOLR_DATA_IMPORT_CLEAN = '&clean='