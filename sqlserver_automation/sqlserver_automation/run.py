import DatabaseConfig
import sqlalchemy
import pandas as pd
import sqlscripts
import dataresult
import convdftohtml
import newSendemail


df_html = []
df_list=dataresult.run(sqlscripts.SCRIPTS,DatabaseConfig.conn_string)
html_list = convdftohtml.run(df_list)
newSendemail.sendEmail(html_list)