class Category(object):
    def __init__(self, id, name):
        """Return a new Category object"""
        self.id = id
        self.name = name
        self.count = 0
        self.sub_categories = []

# <<<<<<< Updated upstream
#     def addSubCategory(self, id, name, count=0):
#         self.sub_categories.append(SubCategory(id, name, count))
# =======
    def addSubCategory(self, id, name, count):
        self.sub_categories.append(SubCategory(id, name, count))
        self.count = self.count + (count if count is not None else 0)

class SubCategory(object):
    def __init__(self, id, name, count=0):
        """Return a new SubCategory object"""
        self.id = id
        self.name = name
        self.count = count if count is not None else 0