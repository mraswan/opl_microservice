from flask_restplus import Api, Resource, fields, reqparse

from opl import oplApi
from opl.oplapi.service.opl_service import OplService

oplns = oplApi.namespace('dynamic', description='OPL APIs')
print("namespace " + oplns.name + " is setup.")

sub_category = oplApi.model('SubCategory', {
    'id': fields.String(attribute='id', description='Sub Category ID'),
    'name': fields.String(attribute='name', description='Sub Category Name'),
})

# marshall with this model, and it handles the multiplicity (array) automatically
#  we need to have a class named "Category", with member field names: "id", "name", "sub_categories"
# this call is found in model package (folder)
category = oplApi.model('Category', {
    'id': fields.String(attribute='id', description='Category ID'),
    'name': fields.String(attribute='name', description='Category Name'),
    'sub_categories': fields.List(fields.Nested(sub_category))
})

lesson = oplApi.model('Lesson', {
    'id': fields.String(attribute='id', description='Lesson ID'),
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

@oplns.route('/lessons')
class LessonController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('query', type=str, help='Query', required=True, location='args')
    '''Matching lessons to a search query'''

    @oplns.doc('list_lessons')
    @oplns.expect(parser, validate=True)
    @oplns.marshal_with(lesson)
    def get(self):
        # relVal = {}
        '''list of lessons'''
        args = LessonController.parser.parse_args()
        service = OplService()
        print(args.get("query"))
        result = service.find_lessons(args.get("query"))
        return result, 200, {'Content-Type': 'application/json; charset=utf8'}

# candidateinfo = oplApi.model('CandidateInfo', {
#     'id': fields.String(attribute='id', description='Candidate ID'),
#     'name': fields.String(attribute='name', description='Candidate Name'),
#     'designation': fields.String(attribute='designation', description='Designation Title'),
#     'expsummary': fields.String(attribute='expsummary', description='Experience Summary'),
#     'industry': fields.String(attribute='industry', description='Industry'),
#     'country': fields.String(attribute='country', description='Country'),
#     'matchscore': fields.Float(attribute='matchscore', description='Match Score')
# })
# jobinfo = oplApi.model('JobInfo', {
#     'id': fields.String(attribute='id', description='Job ID'),
#     'title': fields.String(attribute='title', description='Title'),
#     'description': fields.String(attribute='description', description='Description'),
#     'url': fields.String(attribute='url', description='URL'),
#     'matchscore': fields.Float(attribute='matchscore', description='Match Score'),
#     'titlecategories': fields.String(attribute='title_categories', description='Title Categories'),
#     'descriptioncategories': fields.String(attribute='description_categories', description='Description Categories')
# })
#
# matchedJobs = oplApi.model('FindJobsResponse', {
#     'recordCount': fields.Integer(attribute='recordCount', description='Record Count'),
#     'jobInfos': fields.List(fields.Nested(jobinfo))
# })


# @sugg.route('/enrichedcandidates')
# class EnrichedCandidatesController(Resource):
#     parser = reqparse.RequestParser()
#
#     parser.add_argument('designation', type=str, help='Designation', required=True, location='args')
#     parser.add_argument('designationcategories', type=str, help='Designation Categories', required=False, location='args')
#     parser.add_argument('expsummarycetegories', type=str, help='Exp Summary cetegories', required=False, location='args')
#     '''Matching Enriched Candidate Profiles to a Job'''
#
#     @sugg.doc('list_enrichedcandidates')
#     @sugg.expect(parser, validate=True)
#     @sugg.marshal_with(matchedCandidates)
#     def get(self):
#         '''Auto suggest a list of businesses based on input string'''
#         args = EnrichedCandidatesController.parser.parse_args()
#         service = FindService()
#         print(args.get("designation"))
#         print(args.get("designationcategories"))
#         print(args.get("expsummarycetegories"))
#         results = service.matchEnrichedCandidates(args.get("designation"),
#                                                   "" if (args.get("designationcategories") == None) else args.get("designationcategories"),
#                                                   "" if (args.get("expsummarycetegories") == None) else args.get("expsummarycetegories"))
#         # httpStatusCode = 200
#         # if results.statusCode <> "S_OK":
#         #     httpStatusCode = 404
#         return results
#
# @sugg.route('/candidates')
# class CandidatesController(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('jobtitle', type=str, help='Job Title', required=True, location='args')
#     '''Matching Candidates to a Job'''
#
#     @sugg.doc('list_candidates')
#     @sugg.expect(parser, validate=True)
#     @sugg.marshal_with(matchedCandidates)
#     def get(self):
#         '''Auto suggest a list of businesses based on input string'''
#         args = CandidatesController.parser.parse_args()
#         service = FindService()
#         print(args.get("jobtitle"))
#         results = service.matchCandidates(args.get("jobtitle"))
#         # httpStatusCode = 200
#         # if results.statusCode <> "S_OK":
#         #     httpStatusCode = 404
#         return results
#         # , httpStatusCode