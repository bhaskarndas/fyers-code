import config
from fyers_apiv3 import fyersModel
import datetime
import time


def read_file():
  with open("fyers_access_token.txt", "r") as f:
    token = f.read()
  return token
token=read_file()

fyers = fyersModel.FyersModel(client_id=config.CLIENT_ID, token=token,is_async=False, log_path="")


# Replace with your broker's API library functions

def get_open_positions():
  # Retrieve open positions data from broker and return a list of dictionaries
  resp=fyers.positions()
  if resp['overall']['count_open']!=0:
    open_positions = resp['netPositions']
    return open_positions


def place_stop_loss_order(connection, symbol, quantity, stop_price):
  # Place a stop-loss order for the specified symbol, quantity, and stop price
  pass

# Define stop-loss percentage
stop_loss_percent = 0.1

# Connect to broker
connection = connect_to_broker()

# Get open positions
open_positions = get_open_positions(connection)

# Loop through open positions
for position in open_positions:
  # Calculate stop-loss price based on entry price and stop-loss percentage
  stop_loss_price = position["average_entry_price"] * (1 - stop_loss_percent)

  # Place stop-loss order for the position
  place_stop_loss_order(connection, position["symbol"], position["quantity"], stop_loss_price)

# Close connection (optional, might be handled by the library)
connection.close()

print("Stop-loss orders placed for all open positions.")

def exit_positions():
  global PnL
  traded = "No"

  if traded == "CE":
    SL =  - 2
    while traded == "CE":
      dt = datetime.datetime.now()
      try:
        ltp = getLTP(atmPE)
        if ((ltp > peSL) or (dt.hour >= 15 and dt.minute >= 10)) and ltp != -1:
          oidexitPE = placeOrderFyers(atmPE, "BUY", qty, "MARKET", peSL, "regular")
          PnL = PnL - ltp
          print("Current PnL is: ", PnL)
          df["PE_Exit_Price"] = [ltp]
          print("The OID of Exit PE is: ", oidexitPE)
          traded = "Close"
        else:
          print("PE SL not hit")
          time.sleep(1)

      except:
        print("Couldn't find LTP , RETRYING !!")
        time.sleep(1)


'''
This function applies SL to individual positions rather than calculating the whole sl based on initial capital deployed.

'''





## Under implmentation. Logic to exit single position after stoploss hits
def exit_positions_with_sl():
   # hours, minutes, sl, pos_type = user_input()
    sl=6
    # fetch count of open positions
    positions = fyers.positions()
    pos_count = positions['overall']['count_open']

    # create pandas dataframe for product type 'MIS',NRML or MARGIN(incase of Fyers)
    column_name = 'productType'
    df = pd.DataFrame(positions['netPositions'])
    condition = df[column_name] == 'MARGIN'#pos_type

    # Count the number of rows satisfying the condition condition MIS or NRML
    count = df[condition].shape[0] - 1
    #print(f"Total no. of open positions is {pos_count} and {pos_type} positions is {count}")

    stoploss_pt = df['buyAvg'] * (sl*0.01)

    if df['side'].any()==1:
      df['Stoploss Price'] = df['ltp'].where(df['ltp'] < stoploss_pt, stoploss_pt)
    elif df['side'].any()==-1:
      df['Stoploss Price'] = df['ltp'].where(df['ltp'] > stoploss_pt, stoploss_pt)
    else:
        print('no positions')

    print(df)



