import pandas as pd
import json
import customtkinter
import tkinter as tk
from tkinter import Text
from scripts.ticket_search import conn
from loguru import logger
import better_exceptions

better_exceptions.hook()
better_exceptions.MAX_LENGTH = None
logger.critical('assetLocation')




@logger.catch
class reply(customtkinter.CTkToplevel):
    def __init__(self, titleName, labeltext, populate, heightspec, window_height_spec=300, window_width_spec=650):
        super().__init__()
        self.titleName = titleName
        self.labeltext = labeltext
        self.populate = populate

        # Main Window
        self.title(f"{titleName}")
        if window_width_spec != 650:
            window_width = window_width_spec
        else:
            window_width = 650

        if window_height_spec != 300:
            window_height = window_height_spec
        else:
            window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create textbox
        textbox = Text(self, height=heightspec, width=100, bg="#292929", fg="silver")

        # Create label
        lbl = customtkinter.CTkLabel(self, text=self.labeltext)
        lbl.config()
        # Create an Exit button.
        b1 = customtkinter.CTkButton(self, text="Close", command=self.destroy)

        # Pack the objects
        lbl.pack()
        textbox.pack()
        b1.pack()

        # Creates text in the text box from list
        if self.populate == list:
            for i in self.populate:
                textbox.insert(tk.END, i+'\n')
        else:
            textbox.insert(tk.END, self.populate)
        textbox.config(state='disabled')

    # Start the popUp
    def wait(self):
        try:
            self.wait_window()
        except Exception as e:
            print(e)


