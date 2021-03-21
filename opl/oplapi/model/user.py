from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name, display_name, google_id, profile_pic, user_type_id):
        self.id = id
        self.email = email
        self.name = name
        self.display_name = display_name
        self.google_id = google_id
        self.profile_pic = profile_pic
        self.user_type_id = user_type_id # 1,2,3


class Contributor(User):
    def __init__(self, id, email, name, display_name, google_id, profile_pic, user_type_id, about_me="", lesson_count=0):
        super().__init__(id, email, name, display_name, google_id, profile_pic, user_type_id)
        self.about_me = about_me
        self.lesson_count = lesson_count
        # it is a hash of sub_categories that contributor has contributor and the count of lessons
        self.skills = {}

    #  add sub categories as skills
    def addSkill(self, sub_category_name):
        if sub_category_name not in self.skills:
            self.skills[sub_category_name] = 1
        else:
            self.skills[sub_category_name] = self.skills[sub_category_name] + 1
