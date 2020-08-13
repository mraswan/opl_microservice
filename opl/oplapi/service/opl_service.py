import logging
from opl.oplapi.dataaccess.CategoryDA import CategoryDataAccess
from opl.oplapi.dataaccess.LessonDA import LessonDataAccess

from opl import oplAPIApp as app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OplService(object):
    def __init__(self):
        self.counter = 0
        self.catDA = CategoryDataAccess(app.config['DATABASE_OPL'])
        self.lessonDA = LessonDataAccess(app.config['DATABASE_OPL'])

    #List All Categories and Sub-Categories
    def get_categories(self):
        retval = self.catDA.selectAllCategories()
        return retval

    def get_lessons(self, category_id = None, sub_category_id = None, offset=0, row_count=app.config['SQL_ROW_COUNT']):
        retval = self.lessonDA.selectAllLessons(category_id, sub_category_id, offset, row_count)
        return retval

    def get_lessons_count(self):
        retval = self.lessonDA.selectLessonsCount()
        return retval

    def find_lessons(self, query):
        retval = self.lessonDA.findLessons(query)
        return retval