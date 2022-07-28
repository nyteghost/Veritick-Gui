import customtkinter
from tkinter import *
import tkinter as tk
import sys
from loguru import logger
import better_exceptions


better_exceptions.hook()
better_exceptions.MAX_LENGTH = None
logger.critical('textBox')


@logger.catch
class clientFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.text_frame = customtkinter.CTkFrame(self.frame, corner_radius=10,)
        self.text_frame.grid(row=2, column=0, padx=10, pady=10)

        self.my_text = Text(
            self.text_frame,
            height=60,
            width=67,
            wrap=WORD,
            bd=0,
            bg="#292929",
            fg="silver",
        )

        # self.person_info_box = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        # self.person_info_box.grid(row=2, column=20, padx=10, pady=10)
        # person_info_box_lbl = customtkinter.CTkLabel(self.person_info_box, text="Client Info")
        # person_info_box_lbl.config()
        # person_info_box_lbl.pack()

        self.my_text.pack(fill="both")

    def deleteTF(self, param, param1):
        self.my_text.delete(param, param1)

    def updateTextBox(self, update):
        self.my_text.insert(tk.END, update)


def updateClientBox(update):
    clientFrame.updateTextBox(update)


