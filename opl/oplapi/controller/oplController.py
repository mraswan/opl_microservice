from flask_restplus import Api, Resource, fields, reqparse
from opl import oplAPIApp as app
from opl import oplApi
from opl.oplapi.service.opl_service import OplService
from flask_login import current_user
import requests
from opl import oplOAuth2Client
from flask import redirect, make_response, request, url_for


oplns = oplApi.namespace('dynamic', description='OPL APIs')
print("namespace " + oplns.name + " is setup.")

sub_category = oplApi.model('SubCategory', {
    'id': fields.Integer(attribute='id', description='Sub Category ID'),
    'name': fields.String(attribute='name', description='Sub Category Name'),
    'count': fields.Integer(attribute='count', description='Lesson Count'),
})

# marshall with this model, and it handles the multiplicity (array) automatically
#  we need to have a class named "Category", with member field names: "id", "name", "sub_categories"
# this call is found in model package (folder)
category = oplApi.model('Category', {
    'id': fields.Integer(attribute='id', description='Category ID'),
    'name': fields.String(attribute='name', description='Category Name'),
    'count': fields.Integer(attribute='count', description='Lesson Count'),
    'sub_categories': fields.List(fields.Nested(sub_category))
})

lesson = oplApi.model('Lesson', {
    'id': fields.Integer(attribute='id', description='Lesson ID'),
    'name': fields.String(attribute='name', description='Lesson Name'),
    'description': fields.String(attribute='description', description='Description'),
    'youtube_url': fields.String(attribute='youtube_url', description='youtube_url'),
    'git_url': fields.String(attribute='git_url', description='git_url'),
    'published_timestamp': fields.String(attribute='published_timestamp', description='Category Name'),
    'author_name': fields.String(attribute='author_name', description='Category Name'),
    'category': fields.List(fields.Nested(sub_category)),
    'sub_category': fields.List(fields.Nested(sub_category))
})

lessons = oplApi.model('AllLessons', {
    'recordCount': fields.Integer(attribute='recordCount', description='Record Count'),
    'lessons': fields.List(fields.Nested(lesson))
})

@oplns.route('/categories')
class CategoryController(Resource):

    @oplns.doc('list_categories')
    @oplns.marshal_with(category)
    def get(self):
        # relVal = {}
        '''Auto list of categories and sub_categories'''
        service = OplService()
        result = service.get_categories()
        # relVal["AllCategories"] = result
        return result, 200, {'Content-Type': 'application/json; charset=utf8'}

@oplns.route('/searchlessons')
class LessonSearchController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('query', type=str, help='Query', required=True, location='args')
    '''Matching lessons to a search query'''

    @oplns.doc('list_lessons')
    @oplns.expect(parser, validate=True)
    @oplns.marshal_with(lesson)
    def get(self):
        # relVal = {}
        '''find lessons by name, description, category or subcategory sorted by publish date'''
        args = LessonSearchController.parser.parse_args()
        service = OplService()
        print(args.get("query"))
        result = service.find_lessons(args.get("query"))
        return result, 200, {'Content-Type': 'application/json; charset=utf8'}

@oplns.route('/lessons')
class LessonsController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category', type=int, help='CategoryID', required=False, location='args')
    parser.add_argument('sub_category', type=int, help='SubCategoryID', required=False, location='args')

    @oplns.doc('list_lessons')
    @oplns.expect(parser, validate=True)
    @oplns.marshal_with(lesson)
    def get(self):
        # relVal = {}
        '''list of lessons sorted by publish date'''
        args = LessonsController.parser.parse_args()
        service = OplService()
        print(args.get("category"))
        print(args.get("sub_category"))
        result = service.get_lessons(category_id = args.get("category"), sub_category_id = args.get("sub_category"), offset=0, row_count=app.config['SQL_ROW_COUNT'])
        return result, 200, {'Content-Type': 'application/json; charset=utf8'}

@oplns.route('/lessons/<int:lesson_id>')
class LessonController(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('category', type=int, help='CategoryID', required=False, location='args')
    # parser.add_argument('sub_category', type=int, help='SubCategoryID', required=False, location='args')
    @oplns.doc('lesson_by_id')
    # @oplns.expect(parser, validate=True)
    @oplns.marshal_with(lesson)
    def get(self, lesson_id, **kwargs):
        # relVal = {}
        '''lesson by id'''
        service = OplService()
        result = service.get_lesson(lesson_id = lesson_id)
        if result is None:
            return result, 404, {'Content-Type': 'application/json; charset=utf8'}
        else:
            return result, 200, {'Content-Type': 'application/json; charset=utf8'}

user = oplApi.model('User', {
    'id': fields.Integer(attribute='id', description='User Internal ID'),
    'email': fields.String(attribute='email', description='email'),
    'name': fields.String(attribute='name', description='Name'),
    'display_name': fields.String(attribute='display_name', description='Display Name'),
    'google_id': fields.String(attribute='google_id', description='google_id'),
    'profile_pic': fields.String(attribute='profile_pic', description='profile_pic'),
    'user_type_id': fields.Integer(attribute='user_type_id', description='user_type_id'),
    'is_active': fields.Boolean(attribute='is_active', description='is_active'),
    'is_anonymous': fields.Boolean(attribute='is_anonymous', description='is_anonymous'),
    'is_authenticated': fields.Boolean(attribute='is_authenticated', description='is_authenticated')
})

@oplns.route('/current_user')
class CurrentUserController(Resource):
    @oplns.doc('current_user')
    @oplns.marshal_with(user)
    def get(self):
        print("/current_user -> current_user.is_authenticated: {}".format(current_user.is_authenticated))
        return current_user, 200, {'Content-Type': 'application/json; charset=utf8'}