class BaseResponse(object):
    def __init__(self, code=""):
        self.statusCode = code
        #self.statusDesc = desc