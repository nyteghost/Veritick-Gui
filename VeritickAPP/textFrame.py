import customtkinter
from tkinter import *
import tkinter as tk
import sys
import veriLog
from loguru import logger
import better_exceptions


better_exceptions.hook()
better_exceptions.MAX_LENGTH = None
logger.critical('textBox')


@logger.catch
class TextFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        self.text_frame = customtkinter.CTkFrame(self.frame, corner_radius=10,)
        self.text_frame.grid(row=2, column=0, padx=10, pady=10)

        self.my_text = Text(
            self.text_frame,
            height=600,
            width=67,
            wrap=WORD,
            bd=0,
            bg="#292929",
            fg="silver",
        )

        def redirector(inputStr):
            self.my_text.insert(INSERT, inputStr)
        sys.stdout.write = redirector

        self.my_text.pack(fill="both", expand=True)

    def deleteTF(self, param, param1):
        self.my_text.delete(param, param1)

    def updateTextBox(self, update):
        self.my_text.insert(tk.END, update)
