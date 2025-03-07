Stock Trading Engine Simulation

This project implements a simplified real-time stock trading engine for 1,024 tickers using fixed-size lists (no dictionaries). The core matching algorithm operates in O(n) time per ticker.

Note: The imports (threading, random, and time) are used solely for simulating concurrent trading activity and do not affect the core logic.

How It Works

Order Books:
One list per ticker (T0 to T1023) holds the orders.
Order Matching:
The engine matches buy orders to sell orders based on price criteria (buy price ≥ lowest sell price).
Simulation:
Multiple threads generate random orders and match them concurrently to mimic real-time transactions.
How to Run

Requirements:
Python 3.x
Setup:
Clone or download the repository.
Execution:
Open a terminal in the project directory and run:
python task.py
The simulation will execute and display order and match details.
