class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status, url, apiKey=None, message=None):
        self.status = status
        self.url = url
        self.apiKey = apiKey
        self.message = message


    def __str__(self):
        return "APIError: status={} url={} APIKey={} message={}"\
            .format(self.status)\
            .format(self.url)\
            .format(self.apiKey)\
            .format(self.message)
