import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data(address):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Creds0.json',scope) # get email and key from creds
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key("1PddsYWXx5TfaFWIgt2reDQ2yUwdPvQtmoDmsUSVH8wk").worksheet("Block Owners")
    df = pd.DataFrame.from_dict(sheet.get_all_values())
    df.columns = ['address','no_of_blocks']
    #if address == df['address']
    l = []
    l = df['address']
    if address in df['address']:
        print(True)
    
    return l



print(get_data(0x3e68f91281121a7a4de988d25fed4655d6e3c119))