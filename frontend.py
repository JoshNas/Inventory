import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import information as info
import datetime as dt


engine = create_engine('sqlite:///purchased_items.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
Base.metadata.create_all(engine)


class Purchase(Base):
    __tablename__ = 'sales'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    order_number = Column(Integer)
    date = Column(String)
    name = Column(String(250), nullable=False)
    price = Column(Float)


Base.metadata.create_all(engine)


def get_item(item):
    info.order.append(info.inventory[item])
    display()


def clear_windows():
    item_window.delete(1.0, 'end')
    price_window.delete(1.0, 'end')


def display():
    item_window.delete(1.0, 'end')
    for item in info.order:
        item_window.insert('end', f'{item[1]}  ${item[3]}\n')
    get_total()


def get_total():
    price_window.delete(1.0, 'end')
    pretax_total = 0
    for item in info.order:
        pretax_total += item[3]
    tax = pretax_total * .08
    total = pretax_total + tax
    price_window.insert('end', f'Pretax: {pretax_total}\n')
    price_window.insert('end', f'Tax: {tax}\n')
    price_window.insert('end', f'Total: {total}\n')


def remove_last():
    if len(info.order) > 0:
        info.order.pop()
    display()


def submit():
    with open('order_number', 'r') as file:
        order_num = file.read()

    date = dt.datetime.now()
    for item in info.order:
        new_item = Purchase(order_number=order_num, date=date, name=item[1], price=item[3])
        session.add(new_item)
    session.commit()
    clear_windows()
    info.order = []

    with open('order_number', 'w') as file:
        file.write(str(int(order_num)+1))


root = tk.Tk()
root.geometry('1080x760')
root.title("My Store")

keypad = tk.Canvas()
keypad.grid(row=1, column=0, sticky='nsew')

purchase_window = tk.Canvas()
purchase_window.grid(row=1, column=2, sticky='nsew')

item_window = tk.Text(purchase_window, height=35, width=80)
item_window.grid(row=1, column=0, columnspan=12)

price_window = tk.Text(purchase_window, height=4, width=80)
price_window.grid(row=2, column=0, columnspan=12)


for i in range(len(info.inventory)):
    if i < 7:
        tk.Button(keypad, text=info.inventory[i][1], command=lambda i=i: get_item(i)).grid(row=1, column=i, sticky='nsew')
    elif i < 14:
        tk.Button(keypad, text=info.inventory[i][1], command=lambda i=i: get_item(i)).grid(row=2, column=i-7, sticky='nsew')
    elif i < 21:
        tk.Button(keypad, text=info.inventory[i][1], command=lambda i=i: get_item(i)).grid(row=3, column=i-14, sticky='nsew')
    elif i < 28:
        tk.Button(keypad, text=info.inventory[i][1], command=lambda i=i: get_item(i)).grid(row=4, column=i-21, sticky='nsew')

tk.Button(keypad, text='Remove', command=remove_last).grid(row=16, column=6, sticky='nsew')
tk.Button(keypad, text='Submit', command=submit).grid(row=16, column=7, sticky='nsew')

if __name__ == "__main__":
    root.mainloop()
