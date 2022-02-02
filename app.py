from cv2 import getGaborKernel
import requests
import gspread
import pandas as pd
gc = gspread.oauth()


def get_values():

    id = "1-xdwVAJvSZnLVHM7vkSO3HoGQwPwfO30zrLC8_10Fy4"

    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/' + id)
    worksheet = sht2.worksheet("Sheet1")
    dataframe = pd.DataFrame(worksheet.get_all_records())
    # get data without headers
    data = dataframe.values.tolist()

    return data


# get email and pass from config.txt
with open('config.txt', 'r') as f:
    email = f.readline().strip()
    password = f.readline().strip()


def withdraw_funds(li):

    uri = "https://api.test.barion.com/v2/Withdraw/BankTransfer"

    # create payload and add to request
    payload = {
        "Currency": li[0],
        "Amount": li[1],
        "RecipientName": li[2],
        "Comment": li[3],
        "BankAccount": {
            "AccountNumber": li[4],
            "Format": "GIRO",
            "Country": "HUN",
        }
    }
    # response = requests.get(uri, auth=(email, password))

    # add payload to request
    response = requests.post(uri, json=payload, auth=(email, password))

    if(response.status_code == 200):
        print("Successfully transferred to " +
              li[2] + " with account#: " + li[4])
        print(response.json())


value_li = get_values()[0]
for li in value_li:
    withdraw_funds(li)
