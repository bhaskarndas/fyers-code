import sys
import config
from fyers_apiv3 import fyersModel
import datetime
from datetime import datetime
import time
import pandas as pd


def read_file():
    with open("fyers_access_token.txt", "r") as f:
        token = f.read()
    return token

token=read_file()

fyers = fyersModel.FyersModel(client_id=config.CLIENT_ID, token=token,is_async=False, log_path="")

def user_input():

    #take stoploss value from the user
    sl=float(input("Enter a Stop Loss : "))

    # take product type entry from the user
    position_type=input("Enter position type e.g, MIS or or CNC, NRML. MARGIN, INTRADAY or CNC(for Fyers) :")

    while True:
        # take exit time from the user
        exit_time = input("Enter Exit time in hh:mm format (e.g., 10:15): ")

        try:
            # Parse the time string with desired format (%H:%M) for hours and minutes
            time_obj = datetime.strptime(exit_time, "%H:%M")

            # Access the extracted hours and minutes from the datetime object
            hours = time_obj.hour
            minutes = time_obj.minute

            #print(f"You entered: {hours}:{minutes}")
            break  # Exit the loop if valid
        except ValueError:
            print("Invalid time format. Please enter hh:mm format (e.g., 10:15).")

    return hours,minutes,sl,position_type


def universal_exit():
    hours,minutes,sl,pos_type=user_input()
    # Fetch user Funds
    fund=fyers.funds()

    # Initial Capital
    total_amount = fund['fund_limit'][0]['equityAmount']
    print(f"Initial Capital is Rs. {total_amount}")

    #Utilized Capital
    deployed_capital=fund['fund_limit'][1]['equityAmount']
    print(f"Deployed Capital is Rs. {deployed_capital}")

    # fetch count of open positions
    positions = fyers.positions()
    pos_count = positions['overall']['count_open']

    #create pandas dataframe for product type 'MIS',NRML or MARGIN(incase of Fyers)
    column_name = 'productType'
    df = pd.DataFrame(positions['netPositions'])
    condition = df[column_name] == pos_type



    while count!=0:
        dt = datetime.now()

        #fetch unrealized pnl
        unrealized_pnl=positions['overall']['pl_unrealized']
        # Count the number of rows satisfying the condition condition MIS or NRML
        count = df[condition].shape[0] - 1
        print(f"Total no. of open positions is {pos_count} and {pos_type} positions is {count}")

        if  unrealized_pnl<=(-total_amount*sl*.01):
            print(f"SL hit, exiting all positions. Unrealized PNL :  {unrealized_pnl}")
            fyers.exit_positions()
            sys.exit()
        elif (dt.hour>=hours and dt.minute>=minutes):
            print(f"Exiting all positions at {hours,minutes}")
            fyers.exit_positions()
            sys.exit()
        else:
            print(f"Unrealized PNL : {unrealized_pnl}, SL : {sl}% SL point : {-total_amount*sl*.01} of initial capital {total_amount} . SL not hit")
            time.sleep(1)


if __name__ == "__main__":
    universal_exit()









