import DatabaseConfig
import pandas as pd
import sqlscripts

string = DatabaseConfig.conn_string[0]

string = string.split(';')[1]
print(len(sqlscripts.SCRIPTS))
print(1%5)
df = pd.DataFrame({'server_name':f'{string}'},index = [0])
for index,row in df.iterrows():
    print(row)
