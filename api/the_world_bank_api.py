import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

def make_request():
    url = "https://apigwext.worldbank.org/dvsvc/v1.0/json/APPLICATION/ADOBE_EXPRNCE_MGR/FIRM/SANCTIONED_FIRM"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print("Error haciendo la solicitud:", e)
        return None
def format_data():
    response_data = make_request()
    if response_data:
        dataframe = pd.DataFrame(response_data["response"]["ZPROCSUPP"])
        selected_columns = ["SUPP_NAME", "SUPP_ADDR", "SUPP_CITY", "SUPP_STATE_CODE", "SUPP_ZIP_CODE", 
                            "COUNTRY_NAME", "DEBAR_FROM_DATE", "DEBAR_TO_DATE", "DEBAR_REASON"]
        filtered_df = dataframe[selected_columns]
        filtered_df = filtered_df.fillna("")
        filtered_df.loc[:, "ADDRESS"] = filtered_df["SUPP_ADDR"] + ", " + filtered_df["SUPP_CITY"] + ", " + \
                                        filtered_df["SUPP_STATE_CODE"] + ", " + filtered_df["SUPP_ZIP_CODE"]
        final_columns = ["SUPP_NAME", "ADDRESS", "COUNTRY_NAME", "DEBAR_FROM_DATE", "DEBAR_TO_DATE", "DEBAR_REASON"]
        final_df = filtered_df[final_columns]
        final_df = final_df.rename(columns={
            "SUPP_NAME": "FirmName",
            "ADDRESS": "Address",
            "COUNTRY_NAME": "Country",
            "DEBAR_FROM_DATE": "FromDate",
            "DEBAR_TO_DATE": "ToDate",
            "DEBAR_REASON": "Grounds"
        })
        return final_df
def search_the_world_bank_by_name(name):
    data = format_data()
    if data is None:
        return None
    name_lower = name.lower()
    data["FirmNameLower"] = data["FirmName"].str.lower()
    matches = data[data["FirmNameLower"].str.contains(name_lower, case=False)]
    matches = matches.drop(columns=["FirmNameLower"])
    return matches.to_dict(orient='records')