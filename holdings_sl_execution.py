import sys
import config
from fyers_apiv3 import fyersModel
import datetime
from datetime import datetime
import time
import pandas as pd

sl=6

def read_file():
    with open("fyers_access_token.txt", "r") as f:
        token = f.read()
        fyers_obj = fyersModel.FyersModel(client_id=config.CLIENT_ID, token=token, is_async=False, log_path="")
    return fyers_obj

#fyers=read_file()
#print(fyers.funds())

def get_holdings(sl):
    dt = datetime.now()
    count=1
    fyers = read_file()
    while count!=0:
        holdings=fyers.holdings()

        # Total Investment
        total_investment = holdings['overall']['total_investment']

        #Current valuation of the holdings
        current_valuation=holdings['overall']['total_current_value']

        #pnl percent and total
        pnl_percent=holdings['overall']['pnl_perc']
        total_pnl = holdings['overall']['total_pl']

        #Total number of holdings
        holdings_cnt=holdings['overall']['count_total']

        if total_pnl <= (-total_investment * sl * .01):
            print(f"SL hit, exiting all positions. Notional PNL :  {total_pnl}")
            fyers.exit_positions()
            sys.exit()

        #print(f'''Total Investment is Rs.{total_investment} and current valuation is Rs.{current_valuation}
         #         Profit is {pnl_percent}% and total profit is Rs.{total_pnl}
         #          Total number of holdings is {holdings_cnt}''')
        else:
            print(f"Notional Holding PNL : {total_pnl}, SL : {sl}% SL point : {-total_investment*sl*.01} of initial capital {total_investment} . SL not hit")
            time.sleep(1)

        #print(holdings)

if __name__ == "__main__":
    #universal_exit()
    get_holdings(sl)


