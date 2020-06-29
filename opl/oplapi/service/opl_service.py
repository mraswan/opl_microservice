import logging
from opl.oplapi.dataaccess.CategoryDA import CategoryDataAccess

from opl import oplAPIApp as app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OplService(object):
    def __init__(self):
        self.counter = 0
        self.catDA = CategoryDataAccess(app.config['DATABASE_OPL'])

    #List All Categories and Sub-Categories
    def get_categories(self):
        retval = self.catDA.selectAllCategories()
        return retval