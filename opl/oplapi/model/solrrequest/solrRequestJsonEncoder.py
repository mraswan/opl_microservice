import json
from .suggesterRequest import *


class SolrRequestJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, SuggesterRequest):
            d = {'suggest.q':obj.suggest.q
                  ,'suggest.dictionary':obj.suggest.dictionary
                  ,'wt':obj.wt
                  # ,'indent':'true'
                 }
            return d
        else:
            return json.JSONEncoder.default(self, obj)
            # return obj.__dict__
