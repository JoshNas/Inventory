import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///inventory.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(250), nullable=False)
    count = Column(Integer)
    price = Column(Float)


Base.metadata.create_all(engine)


def add_item():
    name = product_entry.get()
    price = price_entry.get()
    count = count_entry.get()

    if name and price and count:
        new_item = Item(name=name, price=price, count=count)
        session.add(new_item)
        session.commit()

    product_entry.delete(0, 'end')
    price_entry.delete(0, 'end')
    count_entry.delete(0, 'end')


def display_inventory():
    result = session.query('Inventory')
    print(result)


def display_item():
    display_window.delete(1.0, 'end')
    name = product_entry.get()
    price = price_entry.get()
    # count = count_entry.get()

    if name:
        result = session.query(Item).filter_by(name=name).first()
        if result:
            item = f"{result.count} {result.name} \nprice = ${result.price} \n" \
                   f"total value = ${result.count * result.price}"
            display_window.insert('end', item)

    elif price:
        if '>' in price:
            price = price[1:]
            result = session.query(Item).filter(Item.price > price).all()
            for i in result:
                item = f"{i.count} {i.name} \nprice = ${i.price} \n" f"total value = ${i.count * i.price}\n\n"
                display_window.insert('end', item)

    product_entry.delete(0, 'end')
    price_entry.delete(0, 'end')
    count_entry.delete(0, 'end')


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
product_entry = tk.Entry(entry_window, width=40)
product_entry.grid(row=1, column=0, sticky='nsew')
price_entry = tk.Entry(entry_window, width=10)
price_entry.grid(row=1, column=1, sticky='nsew')
count_entry = tk.Entry(entry_window, width=10)
count_entry.grid(row=1, column=2, sticky='nsew')

display_window = tk.Text(height=25, width=40)
display_window.grid(row=1, column=1, sticky='nsew')

keypad = tk.Canvas()
keypad.grid(row=1, column=0, sticky='nsew')

tk.Button(keypad, text='Add', command=add_item).grid(row=0, column=0, sticky='nsew')
tk.Button(keypad, text='Display Item', command=display_item).grid(row=0, column=1, sticky='nsew')
tk.Button(keypad, text='Delete', command=delete_item).grid(row=0, column=2, sticky='nsew')
tk.Button(keypad, text='Display All', command=display_inventory).grid(row=0, column=3, sticky='nsew')


if __name__ == "__main__":
    root.mainloop()
