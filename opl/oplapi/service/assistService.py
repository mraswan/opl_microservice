import json
from ... import rfyAPIApp as app
from ..model.findServiceResponse import *
from watson_developer_cloud import AssistantV1

from ..exception.APIError import APIError
from watson_developer_cloud import WatsonApiException

import requests

class AssistService:
    def __init__(self):
        self.assistant = AssistantV1(
            iam_apikey=app.config['ASSIST_API_KEY'],
            version=app.config['ASSIST_API_VERSION'],
            url='https://gateway-wdc.watsonplatform.net/assistant/api'
        )
        print("Assist Service Initialized")

    def assist(self, jsonPayload=None):
        inputPayLoad = jsonPayload if jsonPayload is not None else {'text': 'Hello'}
        print("Payload is: ".format(inputPayLoad))
        response = None
        try:
            # Invoke a Assistant method
            response = self.assistant.message(
                workspace_id=app.config['ASSIST_WORKSPACE_ID'],
                input=inputPayLoad
            ).get_result()
            # response = self.dummyRespJSON()
        except WatsonApiException as ex:
            print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        else:
            print(json.dumps(response, indent=2))
            # print(response.get_headers())
            # print(response.get_status_code())
        return response


    def dummyRespJSON(self):
        outputStr = '''{
            "intents": [
                {
                    "intent": "Customer_Care_Store_Hours",
                    "confidence": 0.9844614505767824
                }
            ],
            "entities": [],
            "input": {
                "text": "what time are you open"
            },
            "output": {
                "generic": [
                    {
                        "response_type": "text",
                        "text": "Our hours are Monday to Friday 10am to 8pm and Friday and Saturday 11Am to 6pm."
                    }
                ],
                "text": [
                    "Our hours are Monday to Friday 10am to 8pm and Friday and Saturday 11Am to 6pm."
                ],
                "nodes_visited": [
                    "Hours of Operation",
                    "node_6_1482426521282"
                ],
                "log_messages": []
            },
            "context": {
                "conversation_id": "94c1cfba-2723-4094-92c0-e45f49336f8a",
                "system": {
                    "initialized": true,
                    "dialog_stack": [
                        {
                            "dialog_node": "root"
                        }
                    ],
                    "dialog_turn_counter": 4,
                    "dialog_request_counter": 4,
                    "_node_output_map": {
                        "Opening": [
                            0
                        ],
                        "node_1_1495022305143": [
                            0
                        ],
                        "node_3_1522439390442": [
                            0
                        ],
                        "node_6_1482426521282": [
                            0
                        ]
                    },
                    "branch_exited": true,
                    "branch_exited_reason": "completed"
                },
                "no_reservation": true
            }
        }'''

        return json.loads(outputStr)