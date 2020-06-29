from .baseresponse import BaseResponse

class CandidateInfo(object):
    def __init__(self, id, name, designation, expsummary, industry, country, matchscore):
        """Return a new Info object"""
        super(CandidateInfo, self).__init__()
        self.id = id
        self.name = name
        self.designation = designation
        self.expsummary = expsummary
        self.industry = industry
        self.country = country
        self.matchscore = matchscore

class FindCandidatesResponse(BaseResponse):
    def __init__(self, recordCount=0, candidateInfos=None):
        super(FindCandidatesResponse, self).__init__("OK")
        self.recordCount = recordCount
        if candidateInfos is None:
            self.candidateInfos = []
        else:
            self.candidateInfos = candidateInfos

    def setCandidateInfos(self, candidateInfos):
        if candidateInfos is not None:
            self.candidateInfos = candidateInfos


class JobInfo(object):
    def __init__(self, id, title, description, url, matchscore, title_categories, description_categories):
        """Return a new Info object"""
        super(JobInfo, self).__init__()
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.matchscore = matchscore
        self.title_categories = title_categories
        self.description_categories = description_categories

class FindJobsResponse(BaseResponse):
    def __init__(self, recordCount=0, jobInfos=None):
        super(FindJobsResponse, self).__init__("OK")
        self.recordCount = recordCount
        if jobInfos is None:
            self.jobInfos = []
        else:
            self.jobInfos = jobInfos

    def setjobInfos(self, jobInfos):
        if jobInfos is not None:
            self.jobInfos = jobInfos