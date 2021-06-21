import pandas as pd


class Operators(object):

    def __init__(self):
        
        #use pandas to read the google spreadsheet as a csv file, storing the resulting dataframe as an instance variable
        sheet_id = "1zjKv2XGf49tSMeUenmY8NrwuSPx5xBbTUclIkf-YDkM"
        sheet_name = "operator-info"
        URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(sheet_id, sheet_name)

        self.df = pd.read_csv(URL, dtype={'Operator id':str, 'Mode':str})  

    
    def get_operator_by_id(self, operator_id):
        #get row of the dataframe corresponding to the operator_id and return the name of the associated operator
        try:
            operator_name = self.df.loc[self.df['Operator id']==operator_id]['Operator Description'].iloc[0]
            return operator_name
        except:
            return None
        