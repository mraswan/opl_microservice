from baseresponse import BaseResponse

class CandidateMatchResponse(BaseResponse):
    def __init__(self, name="", rin=-1, designation="", summary="", country_code="", code="", desc=""):
        super(CandidateMatchResponse, self).__init__(code, desc)
        self.name = name
        self.rin = rin
        self.designation = designation
        self.summary = summary
        self.country_code = country_code
