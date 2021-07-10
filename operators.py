"""
Copyright 2021 David O'Neill

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
you may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pandas as pd

class Operators(object):


    def __init__(self):
        """Get data from google spreadsheets and store in instance variables
        """
        
        operator_sheet_id = "1zjKv2XGf49tSMeUenmY8NrwuSPx5xBbTUclIkf-YDkM"
        operator_sheet_name = "operator-info"
        operator_URL = "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}".format(operator_sheet_id, operator_sheet_name)
        self.operator_df = pd.read_csv(operator_URL, dtype={"Operator id":str, "Mode":str})  

        mode_sheet_id = "1p3a4vFTbtY21R0V7cksn-orfAqoSIKKkHLOGrByXSMg"
        mode_sheet_name = "mode-info"
        mode_URL = "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}".format(mode_sheet_id, mode_sheet_name)
        self.mode_df = pd.read_csv(mode_URL, dtype={"id":str})


    def get_modes(self):
        """Return json string detailing modes of transport available in line with API specification
        """
        return self.mode_df.to_dict("records")

    
    def populate_json_template(self, operator):
        """Generate data structure to represent operator in line with API specification

        Args:
            operator (dict): dictionary representing operator, generated from Pandas dataframe

        Returns:
            dict: dictionary representing operator in PAS 212 format

        """

        template = {
                "href": "",
                "item-metadata": [
                    {
                        "rel": "urn:X-hypercat:rels:hasDescription:en",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-hypercat:rels:hasHomepage",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasId",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasEmail",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasPhone",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasDefaultLanguage",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasNumberModes",
                        "val": ""
                    },
                 
                    {
                        "rel": "urn:X-opentransport:rels:hasMIPTAURL",
                        "val": ""
                    }
                ]
            }
        
        template["href"] = operator["Open Transport Account API URL"]
        template["item-metadata"][0]["val"] = operator["Operator Description"]
        template["item-metadata"][1]["val"] = operator["Operator URL (homepage)"]
        template["item-metadata"][2]["val"] = operator["Operator id"]
        template["item-metadata"][3]["val"] = operator["Customer Services Contact email"]
        template["item-metadata"][4]["val"] = operator["Customer Services Contact Phone"]
        template["item-metadata"][5]["val"] = operator["Default Language"]
        
        modes = operator["Mode"].split(",")
        template["item-metadata"][6]["val"] = len(modes)
        for i, mode in enumerate(modes):
            mode_details = [{
                        "rel": "urn:X-opentransport:rels:hasMode"+str(i+1)+"#Code",
                        "val": mode
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasMode"+str(i+1)+"#Description",
                        "val": self.mode_df.loc[self.mode_df["id"]==mode]["short-desc"].iloc[0]
                    }]
            template["item-metadata"][-1:-1]=mode_details

        template["item-metadata"][-1]["val"] = operator["Operator MIPTA URL"]

        return template

    
    def get_operator_by_id(self, operator_id="x"):
        """Operator lookup by ID

        Args:
            operator_id (str):passed in through query parameter to represent the id of the operator being fetched - optional

        Returns:
            str: json string representing operator details in PAS212 format

        """
        
        json_result = [
                {
                    "catalogue-metadata": [
                        {
                            "rel": "urn:X-hypercat:rels:isContentType",
                            "val": "application/vnd.hypercat.catalogue+json"
                        },
                        {
                            "rel": "urn:X-hypercat:rels:hasDescription:en",
                            "val": "OpenTransport Operator Catalogue"
                        },
                        {
                            "rel": "urn:X-hypercat:rels:supportsSearch",
                            "val": "urn:X-hypercat:search:simple"
                        }
                    ],
                    "items": [
                        
                    ]
                }
            ]
            
        operator = self.operator_df.loc[self.operator_df["Operator id"]==operator_id]    
        if not operator.empty:
            operator = operator.to_dict("records")[0]
            operator_info = self.populate_json_template(operator)
            json_result[0]["items"].append(operator_info) 
        else:
            operators = self.operator_df.to_dict("records")
            for operator in operators:
                operator_info = self.populate_json_template(operator)
                json_result[0]["items"].append(operator_info)

        return json_result
        