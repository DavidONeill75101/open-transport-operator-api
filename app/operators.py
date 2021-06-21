import pandas as pd
import json

class Operators(object):

    def __init__(self):
        
        #use pandas to read the google spreadsheets as csv files, storing the resulting dataframes as instance variables
        operator_sheet_id = "1zjKv2XGf49tSMeUenmY8NrwuSPx5xBbTUclIkf-YDkM"
        operator_sheet_name = "operator-info"
        operator_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(operator_sheet_id, operator_sheet_name)
        self.operator_df = pd.read_csv(operator_URL, dtype={'Operator id':str, 'Mode':str})  

        mode_sheet_id = "1p3a4vFTbtY21R0V7cksn-orfAqoSIKKkHLOGrByXSMg"
        mode_sheet_name = "mode-info"
        mode_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(mode_sheet_id, mode_sheet_name)
        self.mode_df = pd.read_csv(mode_URL, dtype={'id':str})


    def get_modes(self):
        return json.dumps(self.mode_df.to_dict("records"))


    def populate_json_template(self, operator):
        fields = ['Operator Description', 'Operator URL (homepage)', 'Operator id', 'Customer Services Contact email', 'Customer Services Contact Phone',
        'Default Language', 'Number of Modes', 'Mode', 'Operator MIPTA URL']

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
                        "rel": "urn:X-opentransport:rels:hasMode1#Code",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasMode1#Description",
                        "val": ""
                    },
                    {
                        "rel": "urn:X-opentransport:rels:hasMIPTAURL",
                        "val": ""
                    }
                ]
            }

        template['href'] = operator['Open Transport Account API URL']

        for i in range(len(fields)):
            
            if template[0]['item-metadata'][i]['rel']!='urn:X-opentransport:rels:hasMode1#Description':
                template[0]['item-metadata'][i]['val'] = operator[fields[i]]
            else:
                template[0]['item-metadata'][i]['val'] = self.mode_df.loc[self.mode_df['id']==operator['Mode']]['short-desc'].iloc[0]

        template[0]['item-metadata'][-1]['val'] = operator['Operator MIPTA URL']

        return template


    
    def get_operator_by_id(self, operator_id):
        #get row of the dataframe corresponding to the operator_id and return the name of the associated operator

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
            

        try:
            operator = self.operator_df.loc[self.operator_df['Operator id']==operator_id]
            operator_info = self.populate_json_template(operator)
            json_result[0]['items'].append(operator_info)
            return json_result

        except:
            operators = self.operator_df.to_dict("records")
            for operator in operators:
                operator_info = self.populate_json_template(operator)
                json_result[0]['items'].append(operator_info)
            return json_result