import json
import logging
import os
import configparser
import requests
import pyperclip

# setup initial vars
config = configparser.ConfigParser()
config.read('config.ini')
tftoken = config['App']['TerraformToken']
organization = config['App']['Organization']
aws_access_key_names = config['App']['AwsAccessKeyNames']
aws_secret_key_names = config['App']['AwsSecretKeyNames']
aws_session_token_names = config['App']['AwsSessionTokenNames']
aws_access_key = ""
aws_secret_key = ""
aws_session_token = ""
values = pyperclip.paste()
url = "https://app.terraform.io/api/v2/"
headers = {
    "Authorization": "Bearer " + tftoken,
    "Content-Type": "application/vnd.api+json"
}

# make sure we have the right stuff in the clipboard
if (values.find('export AWS_ACCESS_KEY_ID') < 0):
    print("Unexpected data in your clipboard.")
    exit()

# extract each value and store it
for line in values.splitlines():
    if (line.find('AWS_ACCESS_KEY_ID') >= 0):
        aws_access_key = line.replace("export AWS_ACCESS_KEY_ID=", "")
    if (line.find('AWS_SECRET_ACCESS_KEY') >= 0):
        aws_secret_key = line.replace("export AWS_SECRET_ACCESS_KEY=", "")
    if (line.find('AWS_SESSION_TOKEN') >= 0):
        aws_session_token = line.replace("export AWS_SESSION_TOKEN=", "")

def update_var(wkspid, varid, varname, varvalue, url, headers):
    payload = {
        "data": {
            "id": varid,
            "attributes": {
                "value": varvalue.strip()
            },
            "type":"vars"
        }
    }
    resupd = requests.patch(url + "/workspaces/" + wkspid + "/vars/" + varid, headers = headers, data = json.dumps(payload))
    outupd = json.loads(resupd.text)
    mkey = outupd['data']['attributes']['key']
    mval = outupd['data']['attributes']['value']
    msen = outupd['data']['attributes']['sensitive']
    if msen == True:
        mval = "(sensitive)"
    return mkey + ": " + mval

def replace_values():
    res = requests.get(url + "/organizations/" + organization + "/workspaces", headers = headers)
    wdata = json.loads(res.text)

    # loop through all workspaces in organization
    for data in wdata['data']:
        wksp = data['attributes']['name']
        resvars = requests.get(url + "/workspaces/" + data['id'] + "/vars", headers = headers)
        vars = json.loads(resvars.text)
        vlist = ""
        # loop through var and replace values of interest
        for var in vars['data']:
            cat = var['attributes']['category']
            key = var['attributes']['key']
            val = var['attributes']['value']
            sen = var['attributes']['sensitive']
            varkey = ""
            varval = ""

            if key in aws_access_key_names:
                varkey = key
                varval = aws_access_key
            elif key in aws_secret_key_names:
                varkey = key
                varval = aws_secret_key
            elif key in aws_session_token_names:
                varkey = key
                varval = aws_session_token
            
            # if there's a match, let's do the update!
            if varkey != "":
                out = update_var(data['id'], var['id'], varkey, varval, url, headers)
                vlist = vlist + "    " + out + "\n"

        # quick sanity check to make sure the values were set
        if vlist != "":
            print(wksp)
            print(vlist)

# kick it off
replace_values()
