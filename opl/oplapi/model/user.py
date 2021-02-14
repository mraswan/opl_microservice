from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name, display_name, google_id, profile_pic, user_type_id):
        self.id = id
        self.email = email
        self.name = name
        self.display_name = display_name
        self.google_id = google_id
        self.profile_pic = profile_pic
        self.user_type_id = user_type_id
