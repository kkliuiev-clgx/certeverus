from simple_salesforce import Salesforce
import requests
import pandas as pd
import csv
from io import StringIO

user='steve.stark@certeverus.ai'
pw='GoArmy#211'
sec_token='u0biHPkgRK9OVQGi0t6E2zqq2'
rep_id = '00O3p000005ap9lEAA' 
org = 'https://certeverus.lightning.force.com/'


def salesforce_data(user, pw, sec_token, rep_id, org):
    sf = Salesforce(username=user, password=pw, security_token=sec_token)
    export_params = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
    sf_report_url = org + rep_id + export_params
    response = requests.get(sf_report_url, headers=sf.headers, cookies={'sid': sf.session_id})
    new_report = response.content.decode('utf-8')
    report_df = pd.read_csv(StringIO(new_report))
    print(report_df)

salesforce_data(user, pw, sec_token, rep_id, org)
