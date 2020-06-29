from .baseresponse import BaseResponse

class MatchedCandidate(BaseResponse):
    def __init__(self, job_id="", job_title="", job_description="", distance="", seniority_level="", solr_score="", code=""):
        super(MatchedCandidate, self).__init__(code)
        self.job_id = job_id
        self.job_title = job_title
        self.job_description = job_description
        self.distance = distance
        self.seniority_level = seniority_level
        self.solr_score = solr_score

