from .baseresponse import BaseResponse

class MatchedJobs(BaseResponse):
    def __init__(self, cand_id="", cand_title="", cand_description="", distance="", seniority_level="", solr_score="", code=""):
        super(MatchedJobs, self).__init__(code)
        self.cand_id = cand_id
        self.cand_title = cand_title
        self.cand_description = cand_description
        self.distance = distance
        self.seniority_level = seniority_level
        self.solr_score = solr_score
