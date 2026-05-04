# currency_converter.py

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

API_KEY = 'YOUR_API_KEY'
HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for item in history:
        history_table.insert('', 'end', values=(
            item['from'],
            item['to'],
            item['amount'],
            item['result'],
            item['date']
        ))

def get_currencies():
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()
    return list(data['conversion_rates'].keys())

def convert_currency():
    try:
        source = from_currency.get()
        destination = to_currency.get()
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{source}/{destination}/{amount}'
        response = requests.get(url)
        data = response.json()
        converted_result = data['conversion_result']

        result_label.config(text=f'{amount} {source} = {converted_result} {destination}')
        
        # Сохранение в историю
        history.append({
            'from': source,
            'to': destination,
            'amount': amount,
            'result': converted_result,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_history(history)
        update_history_table()

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Основное окно
root = tk.Tk()
root.title("Currency Converter")
root.geometry("700x500")
root.resizable(False, False)

# Загрузка истории
history = load_history()

# Виджеты
tk.Label(root, text="Из:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="В:").grid(row=0, column=2, padx=10, pady=10)
tk.Label(root, text="Сумма:").grid(row=1, column=0, padx=10, pady=10)

from_currency = ttk.Combobox(root, values=get_currencies())
from_currency.grid(row=0, column=1, padx=10, pady=10)
from_currency.current(0)

to_currency = ttk.Combobox(root, values=get_currencies())
to_currency.grid(row=0, column=3, padx=10, pady=10)
to_currency.current(1)

amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

convert_button = tk.Button(root, text="Конвертировать", command=convert_currency)
convert_button.grid(row=2, column=1, columnspan=2, pady=10)

result_label = tk.Label(root, text="", font=('Arial', 12))
result_label.grid(row=3, column=0, columnspan=4, pady=10)

# Таблица истории
history_table = ttk.Treeview(root, columns=('FROM', 'TO', 'AMOUNT', 'RESULT', 'DATE'), show='headings')
history_table.heading('FROM', text='Из')
history_table.heading('TO', text='В')
history_table.heading('AMOUNT', text='Сумма')
history_table.heading('RESULT', text='Результат')
history_table.heading('DATE', text='Дата')
history_table.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

update_history_table()

root.mainloop()
