import sqlalchemy
import createEngine
import pandas as pd




def run(scripts: list, conn_string) -> list:
    df_list_tot = []
    for conn in conn_string:
        df_list=[]
        # Convert the server name to an IP
        string = conn.split(';')[1]
        df = pd.DataFrame({'server_name':f'{string}'},index = [0])
        #-----------------------------------------------------------------

        
        df_list.append(df)

        #---------------------------------------------------------------
        df_list.append(df)
        myeng = createEngine.runEngine(conn)
        if myeng != None:
            print(myeng.logging_name)
            for script in scripts:
                try:
                    df= pd.read_sql(script,myeng)
                    if df.empty:
                        pass
                    else:
                        df_list.append(df)
                except sqlalchemy.exc.DBAPIError as err:
                    print(err)
                finally:
                    pass
            myeng.dispose()
        df_list_tot.append(df_list)    
    return df_list_tot
        
