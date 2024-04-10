import sys
import config
from fyers_apiv3 import fyersModel
import datetime
from datetime import datetime
import time
import pandas as pd
import holdings_sl_execution as hld
from openpyxl.workbook import Workbook

#Provide exit time here
exit_hours=15
exit_minutes=10

#provide Sl here
sl =6

# uncomment below to take sl input through console
#sl=float(input("Enter a Stop Loss : "))

intraday_data = {
        "segment": [10],
        "side": [1, -1],
        "productType": ["INTRADAY", "CNC"]
    }

def read_file():
    with open("fyers_access_token.txt", "r") as f:
        token = f.read()
    return token

token=read_file()

fyers = fyersModel.FyersModel(client_id=config.CLIENT_ID, token=token,is_async=False, log_path="")
def universal_exit():

    #sl=user_input()

    pos_count = 1

    while pos_count!=0:

        dt = datetime.now()
        #fetch funds
        fund = fyers.funds()

        # Initial Capital
        total_amount = fund['fund_limit'][0]['equityAmount']
        print(f"Initial Capital is Rs. {total_amount}")

        # Utilized Capital
        deployed_capital = fund['fund_limit'][1]['equityAmount']
        print(f"Deployed Capital is Rs. {deployed_capital}")

        # fetch count of open positions
        positions = fyers.positions()
        pos_count = positions['overall']['count_open']

        # create pandas dataframe for product type 'MIS',NRML or MARGIN(incase of Fyers)
        df = pd.DataFrame(positions['netPositions'])

        #fetch unrealized pnl
        unrealized_pnl=positions['overall']['pl_unrealized']

        #print(f"Total no. of open positions is {pos_count} and {pos_type} positions is {count}")
        print(f"Total no. of open positions is {pos_count}")

        if unrealized_pnl<=(-total_amount*sl*.01):
            print(f"SL hit, exiting all positions. Unrealized PNL :  {unrealized_pnl}")
            fyers.exit_positions()
            print("exited all positions")
            sys.exit()

        elif df['productType'].eq('INTRADAY').any() and (dt.hour>=exit_hours and dt.minute>=exit_minutes):
                print(f"Exiting all positions at {exit_hours,exit_minutes}")
                fyers.exit_positions(data=intraday_data)
                sys.exit()
        else:
            print(f"Unrealized PNL : {unrealized_pnl}, SL : {sl}% SL point : {-total_amount*sl*.01} of initial capital {total_amount} . SL not hit")
            time.sleep(1)

if __name__ == "__main__":
    universal_exit()
