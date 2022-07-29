import customtkinter
import tkinter as tk
import sys
import os
import threading
from scripts.veritick import main_run
from _skeleton.textFrame import TextFrame
from _skeleton.clientInfoFrame import clientFrame
from loguru import logger
import better_exceptions
from concurrent.futures import ThreadPoolExecutor
better_exceptions.hook()
better_exceptions.MAX_LENGTH = None
logger.critical('mainWindow')


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


img_dir = resource_path("../images")

img_file = img_dir + "/sca-logo.jpg"


@logger.catch
class vtKinterClass(customtkinter.CTk):
    def __init__(self, update=""):
        super().__init__()
        self.title("VeriTick")
        self.update = update
        # Main Window
        # self.geometry(f"{600}x{1150}")
        window_width = 850
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # Main Frame
        self.MainFrame = customtkinter.CTkFrame(self, corner_radius=10, height=window_height, width=window_width)
        # self.MainFrame.pack(pady=20, expand=True)
        self.MainFrame.grid(rowspan=5, columnspan=5, pady=20, sticky="n,e,s,w")
        # CMD Redirect Frame
        self.text_frame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10,)
        self.my_text = TextFrame(self.MainFrame, self.text_frame)
        self.text_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n,e,s,w")




        # Info Box
        # self.client_info_frame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10,)
        # self.client_info = clientFrame(self.MainFrame, self.client_info_frame)
        # self.client_info_frame.grid(row=2, column=1, padx=10, pady=10)

        # Ticket Entry Section
        self.ticketEntryFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.ticketEntryFrame.grid(row=0, column=0, padx=10, pady=10, sticky="n,e,s,w")

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
            command=lambda: threading.Thread(target=self.veritick_on_press).start())
            # command=self.threading)
        self.my_button.grid(row=0, column=1, padx=10)

        # Switch Section
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

        self.switch_2 = customtkinter.CTkSwitch(
            self.switch_frame,
            text="Student",
            command=self.switch_event2,
            onvalue="on",
            offvalue="off",
            bg_color="#2A2D2E",
        )
        self.switch_1.deselect()
        self.switch_2.deselect()

        self.switch_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.switch_2.grid(row=0, column=1, padx=10, pady=10, sticky="w")


    def threading(self):
        threading.Thread(target=self.veritick_on_press).start()


    def veritick_on_press(self):
        value = self.ticketEntry.get().strip()
        switch_state = self.switch_event()
        switch_state2 = self.switch_event2()
        if not value:
            print("You didn't enter anything!")
        else:
            print("*******************************************************")
            # _thread.start_new_thread(main_run,(value,switch_state))
            main_run(value, switch_state, switch_state2)
            # threading.Thread(target=main_run(value, switch_state)).start()

    def switch_event(self):
        self.my_text.deleteTF("1.0", "end")
        if self.switch_1.get() == "on":
            switch_state = 1
        else:
            switch_state = 0
        return switch_state

    def switch_event2(self):
        self.my_text.deleteTF("1.0", "end")
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
