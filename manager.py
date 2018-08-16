import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from database import Base, Item

engine = create_engine('sqlite:///sqlalchemy_inventory.db')


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()


def add_item():
    item = item_entry.get()
    price = price_entry.get()
    count = count_entry.get()

    if item and price and count:
        new_item = Item(name=item, price=price, count=count)
        s.add(new_item)
        s.commit()

    item_entry.delete(0, 'end')
    price_entry.delete(0, 'end')
    count_entry.delete(0, 'end')


def display_inventory():
    result = s.query('Inventory')
    print(result)


def delete_item():
    pass


root = tk.Tk()
root.geometry('1080x760')
root.title('Manager')

entry_window = tk.Canvas(root)
entry_window.grid(row=0, column=0)
tk.Label(entry_window, text='Item').grid(row=0, column=0, sticky='nsew')
tk.Label(entry_window, text='Price').grid(row=0, column=1, sticky='nsew')
tk.Label(entry_window, text='Count').grid(row=0, column=2, sticky='nsew')
item_entry = tk.Entry(entry_window, width=40)
item_entry.grid(row=1, column=0, sticky='nsew')
price_entry = tk.Entry(entry_window, width=10)
price_entry.grid(row=1, column=1, sticky='nsew')
count_entry = tk.Entry(entry_window, width=10)
count_entry.grid(row=1, column=2, sticky='nsew')

keypad = tk.Canvas()
keypad.grid(row=1, column=0, sticky='nsew')

tk.Button(keypad, text='Add', command=add_item).grid(row=0, column=0, sticky='nsew')
tk.Button(keypad, text='Display', command=display_inventory).grid(row=0, column=1, sticky='nsew')
tk.Button(keypad, text='Delete', command=delete_item).grid(row=0, column=2, sticky='nsew')


if __name__ == "__main__":
    root.mainloop()
