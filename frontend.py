import tkinter as tk
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select

engine = create_engine('sqlite:///inventory.db')
metadata = MetaData()
table = Table('items', metadata, autoload=True, autoload_with=engine)

s = select([table])
my_inventory = engine.execute(s)
inventory = []
for i in my_inventory:
    inventory.append(i)

print(inventory)


def get_item(item):
    print(inventory[item])


root = tk.Tk()
root.geometry('1080x760')
root.title("My Store")

message = tk.Text(root, height=1, width=80)
message.grid(row=0, column=0)

keypad = tk.Canvas()
keypad.grid(row=1, column=0, sticky='nsew')

order_window = tk.Canvas()
order_window.grid(row=1, column=2, sticky='nsew')

table_window = tk.Text(order_window, height=3, width=80)
table_window.grid(row=0, column=2, sticky='nsew')

item_window = tk.Text(order_window, height=35, width=80)
item_window.grid(row=1, column=0, columnspan=12)

price_window = tk.Text(order_window, height=4, width=80)
price_window.grid(row=2, column=0, columnspan=12)

tk.Button(keypad, text=inventory[0][1], command=lambda: get_item(0)).grid(row=1, column=0, sticky='nsew')








if __name__ == "__main__":
    root.mainloop()