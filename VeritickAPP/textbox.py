import customtkinter
from tkinter import *
import sys


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
