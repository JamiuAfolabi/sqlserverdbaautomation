import pandas as pd
import sqlscripts

def convertHeader(df):
    name = df.loc[0,'server_name']
    #html_tab=df.to_html(classes='table table-striped',index=False)
    html='''\
        <html>
            <head>
            </head>
            <body>
                <br>
                <h3>{0}<h3>
                <br>
                <hr>
            </body>
        </html>
        '''.format(name)
    return html


def convertNormal(df):
    """
    PARAMETER
    ---------
    df: dataframe

    RETURNS
    --------
    html: dataframe converted to html
    """
    html_tab=df.to_html(classes='table table-striped',index=False)
    html='''\
        <html>
            <head>
                <style>
                table, th, td {{
                    border: 1px solid black;
                    border-collapse: collapse;
                    }}
                    th, td {{
                        padding: 5px;
                        text-align: left;    
                    }}  
                </style>
            </head>
            <body>
                <br>
                {0}
            </body>
        </html>
        '''.format(html_tab)
    return html

def run(df_list_total: list,html_list=[]) -> list:
    
    
    lst = html_list

    for df_list in df_list_total:
        #-------------------------------------------------------------------------------
        if len(df_list) != 0:
            counter = 0
            for df in df_list:
                if counter == 0:
                    df_htm = convertHeader(df)
                    lst.append(df_htm)
                else :   
                    df_htm = convertNormal(df)
                    lst.append(df_htm)
                counter = counter + 1
    return lst            
        #     return lst
        # else:
        #     return []





