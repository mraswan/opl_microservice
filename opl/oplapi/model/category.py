class Category(object):
    def __init__(self, id, name):
        """Return a new Category object"""
        self.id = id
        self.name = name
        self.sub_categories = []

    def addSubCategory(self, id, name):
        self.sub_categories.append(SubCategory(id, name))

class SubCategory(object):
    def __init__(self, id, name):
        """Return a new SubCategory object"""
        self.id = id
        self.name = name