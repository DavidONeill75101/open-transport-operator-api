import pandas as pd

sheet_id = "1zjKv2XGf49tSMeUenmY8NrwuSPx5xBbTUclIkf-YDkM"
sheet_name = "operator-info"
URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
	sheet_id,
	sheet_name
)

df = pd.read_csv(URL, dtype={'Operator id':str, 'Mode':str})


try:
    print(df.loc[df['Operator id']=='020']['Operator Description'].iloc[0])
except:
    print("not possible")

