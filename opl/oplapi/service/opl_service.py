import logging
from opl.oplapi.dataaccess.CategoryDA import CategoryDataAccess
from opl.oplapi.dataaccess.LessonDA import LessonDataAccess
from opl.oplapi.dataaccess.UserDA import UserDataAccess

from opl import oplAPIApp as app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OplService(object):
    def __init__(self):
        self.counter = 0
        self.catDA = CategoryDataAccess(app.config['DATABASE_OPL'])
        self.lessonDA = LessonDataAccess(app.config['DATABASE_OPL'])
        self.userDA = UserDataAccess(app.config['DATABASE_OPL'])

    #List All Categories and Sub-Categories
    def get_categories(self):
        retval = self.catDA.selectAllCategories()
        return retval

    def get_lessons(self, category_id = None, sub_category_id = None, offset=0, row_count=app.config['SQL_ROW_COUNT']):
        retval = self.lessonDA.selectAllLessons(category_id, sub_category_id, offset, row_count)
        return retval

    def get_lesson(self, lesson_id):
        retval = self.lessonDA.selectLessonById(lesson_id)
        return retval

    def get_lessons_count(self):
        retval = self.lessonDA.selectLessonsCount()
        return retval

    def find_lessons(self, query):
        retval = self.lessonDA.findLessons(query)
        return retval

    def get_contributors(self):
        contributors = self.userDA.selectContributors()
        contributors_sills = self.userDA.selectContributorsAndSkills()
        for contributor in contributors:
            for (skill_name,skill_count) in contributors_sills[contributor.id].items():
                contributor.addSkillWithCount(skill_name, skill_count)
        return contributors

    def get_contributor(self, user_id):
        contributor = self.userDA.selectContributorByUserId(user_id)
        lessons = self.lessonDA.selectLessonByUserId(user_id)
        for lesson in lessons:
            contributor.addSkill(lesson.sub_category.name)
        return contributor

    def get_contributor_by_user_handle(self, user_handle):
        contributor = self.userDA.selectContributorByUserhandle(user_handle)
        if contributor is not None:
            lessons = self.lessonDA.selectLessonByUserId(contributor.id)
            for lesson in lessons:
                contributor.addSkill(lesson.sub_category.name)
        return contributor

    def get_lessons_by_user(self, user_id):
        retval = self.lessonDA.selectLessonByUserId(user_id)
        return retval

    def get_lessons_by_user_handle(self, user_handle):
        retval = self.lessonDA.selectLessonByUserHandle(user_handle)
        return retval
