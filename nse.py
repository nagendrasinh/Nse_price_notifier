from nsetools import Nse
import datetime
import threading
from time import gmtime, strftime, localtime
import sys, os
import argparse
import notify2
import pytz
import pandas as pd
import keyboard
from beepy import beep
sys.tracebacklimit = 0


df = pd.read_csv("trade.csv")
"""
if len(sys.argv) >4 :

        print('You have specified too many arguments')
        sys.exit()

if len(sys.argv) < 2 :

        print('You have specified less arguments')
        sys.exit()

my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('names',type=str,help='the path to list')
my_parser.add_argument('price_t',type=float,help='the path to list')
args = my_parser.parse_args()
"""


# using now() to get current time
# Update 't' variable to ne
def notifi(name_stock, price):
    ICON_PATH = "icon.png"#icon path
    notify2.init("Stock Notifier")
    n = notify2.Notification(name_stock, price, icon=ICON_PATH)
    # set urgency level
    n.set_urgency(notify2.URGENCY_NORMAL)
    # set timeout for a notification
    n.set_timeout(100)
    beep(sound=4)
    n.show()


def one_minute_close():

    while True:

        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

        if current_time.second == 59:

            return s["lastPrice"]


keep_going = True


def continous_price(names, target_buy,target_sell, lock):

    s = nse.get_quote(names)
    #   lock.acquire()
    while keep_going:
        print(float(s["lastPrice"]))
        try:
            print(float(s["lastPrice"])) 	
            print(float(target_buy)) 
           # print(s["lastPrice"])
            if float(s["lastPrice"]) == float(target_buy) :
                
                notifi(str(names), str(target_buy) + " price in range")
                break
            elif float(s["lastPrice"]) == float(target_sell):
             
                notifi(str(names), str(target_buy )+ " price in range")
                break

        except KeyboardInterrupt:

            print("Interrupted")

            sys.exit(0)
        

def mlp(names, price_buy,price_sell ,lock):

    return threading.Thread(
        target=continous_price, args=(names, price_buy,price_sell, lock)
    )  # ,daemon=True


if __name__ == "__main__":
    current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

    nse = Nse()
    lock = threading.Lock()
    for i in range(len(df.index)):

        i = mlp(df.iloc[i]["equity"], df.iloc[i]["target_price_buy"],df.iloc[i]["target_price_sell"],lock) 
        i.start()
      
