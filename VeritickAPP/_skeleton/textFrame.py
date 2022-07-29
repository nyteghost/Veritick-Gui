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
class TextFrame:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.text_frame = customtkinter.CTkFrame(self.frame, corner_radius=10,)
        self.text_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n,e,s,w")

        self.v = Scrollbar(self.text_frame, orient='vertical')
        self.v.pack(side=RIGHT, fill='y')

        self.my_text = Text(
            self.text_frame,
            wrap=WORD,
            bd=0,
            bg="#292929",
            fg="silver",
        )

        def redirector(inputStr):
            try:
                self.my_text.insert(INSERT, inputStr)
            except Exception:
                raise Exception('Exit')
        sys.stdout.write = redirector

        self.v.config(command=self.my_text.yview)
        self.my_text.pack(fill="both")

    def deleteTF(self, param, param1):
        self.my_text.delete(param, param1)

    def updateTextBox(self, update):
        self.my_text.insert(tk.END, update)
