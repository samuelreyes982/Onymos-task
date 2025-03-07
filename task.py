'''
The following imports are only used in the simulation
'''
import threading
import random
import time

# Total number of tickers supported.
NUM_TICKERS = 1024

tickers = [f"T{i}" for i in range(NUM_TICKERS)]
# Create an order book: a list of lists; one list per ticker.
orderBooks = [[] for _ in range(NUM_TICKERS)]

# Global order counter (using the GIL, simple integer increments are safe here).
order_id_counter = 0

class Order:
    def __init__(self, order_id, order_type, ticker, quantity, price):
        self.order_id = order_id         
        self.order_type = order_type      
        self.ticker = ticker              
        self.quantity = quantity         
        self.price = price               
        self.active = True                
# Helper: map ticker symbol to index in the orderBooks array.
def ticker_to_index(ticker):
    # We assume ticker is in the form "T<number>"
    try:
        index = int(ticker[1:])
        if 0 <= index < NUM_TICKERS:
            return index
    except:
        pass
    return None

def addOrder(order_type, ticker, quantity, price):
    
    global order_id_counter
    
    order_id = order_id_counter
    order_id_counter += 1
    order = Order(order_id, order_type, ticker, quantity, price)
    idx = ticker_to_index(ticker)
    if idx is None:
        print(f"Invalid ticker {ticker}")
        return
   
    orderBooks[idx].append(order)
    print(f"Added {order_type} order: id={order_id}, ticker={ticker}, qty={quantity}, price={price}")

def matchOrder(ticker):
    
    idx = ticker_to_index(ticker)
    if idx is None:
        print(f"Invalid ticker {ticker} in matchOrder")
        return
    orders = orderBooks[idx]
    
   
    buy_orders = []
    sell_orders = []
    for order in orders:
        if order.active and order.quantity > 0:
            if order.order_type == "Buy":
                buy_orders.append(order)
            elif order.order_type == "Sell":
                sell_orders.append(order)
                
    # If no orders to match, exit.
    if not sell_orders or not buy_orders:
        return

    # Find the Sell order with the lowest price.
    lowest_sell = None
    for order in sell_orders:
        if lowest_sell is None or order.price < lowest_sell.price:
            lowest_sell = order

    # Look for any Buy order with a price >= lowest_sell.price.
    matching_buy = None
    for order in buy_orders:
        if order.price >= lowest_sell.price:
            matching_buy = order
            break

    # If no matching Buy order exists, no match can occur.
    if matching_buy is None:
        return

    # Determine the quantity to trade.
    traded_quantity = min(matching_buy.quantity, lowest_sell.quantity)
    matching_buy.quantity -= traded_quantity
    lowest_sell.quantity -= traded_quantity

    print(f"Matched ticker {ticker}: Buy order {matching_buy.order_id} and Sell order {lowest_sell.order_id} for quantity {traded_quantity} at price {lowest_sell.price}")

    # Mark orders as inactive if fully filled.
    if matching_buy.quantity == 0:
        matching_buy.active = False
    if lowest_sell.quantity == 0:
        lowest_sell.active = False

def order_generator():
    
    while True:
        order_type = random.choice(["Buy", "Sell"])
       
        ticker_index = random.randint(0, NUM_TICKERS - 1)
        ticker = tickers[ticker_index]
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)
        addOrder(order_type, ticker, quantity, price)
        
        time.sleep(random.uniform(0.01, 0.1))

def order_matcher():
    
    while True:
        ticker_index = random.randint(0, NUM_TICKERS - 1)
        ticker = tickers[ticker_index]
        matchOrder(ticker)
        time.sleep(random.uniform(0.01, 0.1))

# sample simulation
num_generator_threads = 5  
num_matcher_threads = 3    
threads = []

for _ in range(num_generator_threads):
    t = threading.Thread(target=order_generator)
    t.daemon = True
    threads.append(t)
    t.start()

for _ in range(num_matcher_threads):
    t = threading.Thread(target=order_matcher)
    t.daemon = True
    threads.append(t)
    t.start()


time.sleep(5)
print("Simulation complete.")
