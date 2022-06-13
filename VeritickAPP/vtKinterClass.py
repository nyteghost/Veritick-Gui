from tkinter import *
import customtkinter
import sys
import os
import threading
import queue
from concurrent.futures import process
from loguru import logger
from veritick import main_run
process.__name__

logger.add("./logs/vtKinterClass.log", backtrace=True, diagnose=True, rotation="12:00")

q = queue.Queue()


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


img_dir = resource_path("images")

img_file = img_dir + "./sca-logo.jpg"


class vtKinterClass(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("VeriTick")

        # Main Window
        self.geometry(f"{1200}x{1070}")

        # Main Frame
        self.MainFrame = customtkinter.CTkFrame(
            self, corner_radius=10, width=1000, height=500
        )
        self.MainFrame.pack(pady=20, expand=True)

        self.text_frame = customtkinter.CTkFrame(
            self.MainFrame,
            corner_radius=10,
        )
        self.text_frame.grid(row=2, column=0, padx=10, pady=10)

        # CMD Redirect Frame
        self.my_text = Text(
            self.text_frame,
            height=600,
            width=67,
            wrap=WORD,
            bd=0,
            bg="#292929",
            fg="silver",
        )

        # Ticket Entry Section
        self.ticketEntryFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.ticketEntryFrame.grid(row=0, column=0, padx=10, pady=10)

        self.ticketEntry = customtkinter.CTkEntry(
            self.ticketEntryFrame,
            width=400,
            height=40,
            border_width=1,
            placeholder_text="Enter Ticket Number",
            text_color="silver",
        )
        self.ticketEntry.grid(row=0, column=0, padx=10, pady=10)

        self.my_button = customtkinter.CTkButton(
            self.ticketEntryFrame,
            text="Lookup",
            command=lambda: threading.Thread(target=self.veritick_on_press).start(),
        )
        self.my_button.grid(row=0, column=1, padx=10)

        # CMD Redirect Frame
        self.switch_frame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.switch_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.switch_1 = customtkinter.CTkSwitch(
            self.switch_frame,
            text="MU Update",
            command=self.switch_event,
            onvalue="on",
            offvalue="off",
            bg_color="#2A2D2E",
        )
        self.switch_1.deselect()
        self.switch_1.pack()

        self.my_text.pack(fill="both", expand=True)

        def redirector(inputStr):
            self.my_text.insert(INSERT, inputStr)

        sys.stdout.write = redirector

    def veritick_on_press(self):
        value = self.ticketEntry.get().strip()
        switch_state = self.switch_event()
        if not value:
            print("You didn't enter anything!")
        else:
            print("*******************************************************")
            # _thread.start_new_thread(main_run,(value,switch_state))
            main_run(value, switch_state)

    def switch_event(self):
        self.my_text.delete("1.0", "end")
        if self.switch_1.get() == "on":
            switch_state = 1
        else:
            switch_state = 0
        return switch_state

    def start(self):
        self.mainloop()


# if __name__ == '__main__':
#     app = vtKinterClass()
#     app.mainloop()
# try:
#     _thread.start_new_thread(root.mainloop(),())
# except AttributeError as ex:
#     if str(ex) == "'_tkinter.tkapp' object has no attribute 'root'":
#         pass
