import json
from .baseRequest import BaseRequest

class SuggesterRequest(BaseRequest):
    def __init__(self, suggest, wt="json", indent=True):
        BaseRequest.__init__(self, wt, indent)
        self.suggest = suggest
        self.shardsEnabled = True



