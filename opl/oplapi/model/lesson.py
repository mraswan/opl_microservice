from .category import Category, SubCategory

class Lesson(object):
    def __init__(self, id, name, description, youtube_url, git_url, published_timestamp,
                 category_id, category_name, sub_category_id, sub_category_name,
                 author_name):
        """Return a new Category object"""
        self.id = id
        self.name = name
        self.description = description
        self.youtube_url = youtube_url
        self.git_url = git_url
        self.published_timestamp = published_timestamp
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.author_name = author_name
        self.category = Category(category_id, category_name)
        self.sub_category = SubCategory(sub_category_id, sub_category_name)

    # def addSubCategory(self, id, name):
    #     self.sub_categories.append(SubCategory(id, name))
