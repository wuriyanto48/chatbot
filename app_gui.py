#!/usr/bin/env python

import tkinter as tk

from core.model import load_model
from core.bot import do_answer

def run_window():
    model, (words, labels, training, output) = load_model()

    main_window = tk.Tk(screenName='MainScreen')
    main_window.title('Chat with Bot')
    main_window.geometry("950x600+300+300")

    menu = tk.Menu(master=main_window)
    main_window.config(menu=menu, background='#75bdbd')

    file_menu = tk.Menu(master=menu)

    menu.add_cascade(label='Chatbot', menu=file_menu)
    file_menu.add_command(label='About')
    menu.add_separator()
    file_menu.add_command(label='Exit', command=main_window.quit)

    label_1 = tk.Label(master=main_window, text='Pesanmu : ')
    label_1.grid(row=0)

    entry_1_text = tk.StringVar()
    entry_1 = tk.Entry(master=main_window, width=80, textvariable=entry_1_text)
    entry_1.grid(row=0, column=1)
    
    scrollbar = tk.Scrollbar(master=main_window, orient='vertical')
    scrollbar.grid(row=3, column=2)

    list_box = tk.Listbox(master=main_window, width=80, yscrollcommand = scrollbar.set)
    list_box.grid(row=3, column=1)

    def btn_1_click():
        if entry_1_text.get() != '':
            sentence = entry_1_text.get()
            answ = do_answer(sentence)

            list_box.insert(tk.END, 'Aku: {}'.format(sentence))
            list_box.insert(tk.END, 'Bot: {}'.format(answ))
            entry_1_text.set('')

    btn_1 = tk.Button(master=main_window, text='Send', width=10, command=btn_1_click)
    btn_1.config(background='#0fa4d6')
    btn_1.grid(row=0, column=3)

    main_window.mainloop()

if __name__ == '__main__':
    run_window()