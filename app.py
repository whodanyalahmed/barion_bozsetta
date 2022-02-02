import requests
import gspread
import pandas as pd
import datetime
# add logger


logFile = open("log.txt", "a+")

logFile.write("\nStarted at: " + str(datetime.datetime.now()))


gc = gspread.oauth()


def get_values(id):


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

    # if(response.Errors == []):

    errors = response.json()['Errors']
    # get description from Errors
    if(errors == []):

        if(response.status_code == 200):
            print("Success: Successfully transferred to " +
                  li[2] + " with account#: " + li[4])
            logFile.write("\nSucess: Successfully transferred to " +
                          li[2] + " with account#: " + li[4])

    # get Errors from response
    else:
        description = errors[0]['Description']

        print("Error: " + str(description) + " with account#: " + li[4])
        logFile.write("\nError: " + str(description) +
                      " with account#: " + li[4])


id = "1-xdwVAJvSZnLVHM7vkSO3HoGQwPwfO30zrLC8_10Fy4"
value_li = get_values(id)
for li in value_li:
    withdraw_funds(li)

# close file
logFile.write("\nFinished at: " + str(datetime.datetime.now()))
logFile.close()
