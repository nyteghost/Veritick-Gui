import tkinter
import customtkinter
import better_exceptions
import veriLog
from loguru import logger

# Settings
better_exceptions.hook()
better_exceptions.MAX_LENGTH = None
logger.critical('popUpBox')


@logger.catch
class equipPopUp(customtkinter.CTkToplevel):
    def __init__(self, titleName, staff, labelFound="", included=""):
        super().__init__()
        self.rlm = None
        self.RFRI = None
        self.ERI = None
        self.label_radio_group3 = None
        self.label_radio_group2 = None
        self.my_button = None
        self.rfrBTNList = []
        self.printBTNList = []

        self.labelFound = labelFound
        self.staff = staff
        self.included = included

        if self.staff == 0:
            self.status = "Student"
        elif self.staff == 1:
            self.status = "Staff"

        self.titleName = titleName

        # Main Window
        self.title(f"{titleName}")
        window_width = 750
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.btn1 = tkinter.StringVar()
        self.btn2 = tkinter.StringVar()
        self.btn3 = tkinter.StringVar()

        self.label_radio_group = customtkinter.CTkLabel(
            master=self, text="Please Select Request Equipment:"
        )
        self.label_radio_group.grid(row=0, column=0, sticky="nw")

        if self.labelFound == "N":
            z = 0
            Equipment_Requested = [
                "Print Return Label at SCA",
                "Email Electronic Return Label",
                "Email Electronic Return Label",
            ]
            for i in Equipment_Requested:
                z += 1
                self.radio_button = customtkinter.CTkRadioButton(
                    master=self, text=i, variable=self.btn3, value=z
                )
                self.radio_button.grid(row=z, column=0, sticky="nw")

            x = 0
            Equipment_Requested = [
                f"Replacement {self.status} Kit",
                f"Replacement {self.status} Printer",
                "Charger",
            ]
            for i in Equipment_Requested:
                x += 1
                self.radio_button = customtkinter.CTkRadioButton(
                    master=self,
                    text=i,
                    variable=self.btn1,
                    value=x,
                    command=self.submitButton,
                )
                self.radio_button.grid(row=x, column=1, sticky="nw")
        else:
            if self.included == "RFRI":
                self.createRFRBtns()
            elif self.ncluded == 2:
                self.createPrinterChoices()
            elif self.included == 3:
                pass

    def createLabelBtns(self):
        y = 0
        ra = self.label_radio_group2 = customtkinter.CTkLabel(
            master=self, text="Please Select Reason for Return:"
        )
        self.label_radio_group2.grid(row=0, column=2, sticky="nw")
        self.rfrBTNList.append(ra)
        rlm = ["Print Return Label at SCA", "Email Electronic Return Label"]
        for i in rlm:
            y += 1
            rb = self.radio_button = customtkinter.CTkRadioButton(
                master=self, text=i, variable=self.btn3, value=y
            )
            self.radio_button.grid(row=y, column=2, sticky="nw")
            self.rfrBTNList.append(rb)

    def createRFRBtns(self):
        y = 0
        ra = self.label_radio_group2 = customtkinter.CTkLabel(
            master=self, text="Please Select Reason for Return:"
        )
        self.label_radio_group2.grid(row=0, column=2, sticky="nw")
        self.rfrBTNList.append(ra)
        equipment_reason_for_return = [
            "Display",
            "OS/MB",
            "Keyboard",
            "Camera",
            "Audio/Mic",
            "Battery",
            "Physical Damage",
        ]
        for i in equipment_reason_for_return:
            y += 1
            rb = self.radio_button = customtkinter.CTkRadioButton(
                master=self, text=i, variable=self.btn2, value=y
            )
            self.radio_button.grid(row=y, column=2, sticky="nw")
            self.rfrBTNList.append(rb)

        self.my_button = customtkinter.CTkButton(
            master=self, text="Submit", command=self.destroy
        )
        self.my_button.grid(row=8, column=2, sticky="nw")

    def createPrinterChoices(self):
        y = 0
        ra = self.label_radio_group3 = customtkinter.CTkLabel(
            master=self, text="Please Select Reason for Return of Printer:"
        )
        self.label_radio_group3.grid(row=0, column=2, sticky="nw")
        self.printBTNList.append(ra)
        equipment_reason_for_return = ["Hardware", "Software"]
        for i in equipment_reason_for_return:
            y += 1
            rb = self.radio_button = customtkinter.CTkRadioButton(
                master=self, text=i, variable=self.btn2, value=y
            )
            self.radio_button.grid(row=y, column=2, sticky="nw")
            self.printBTNList.append(rb)

        self.my_button = customtkinter.CTkButton(
            master=self, text="Submit", command=self.destroy
        )
        self.my_button.grid(row=8, column=2, sticky="nw")

    def submitButton(self):
        if self.btn1.get() == "1":
            for widget in self.printBTNList:
                widget.grid_remove()
            self.createRFRBtns()
        if self.btn1.get() == "2":
            for widget in self.rfrBTNList:
                widget.grid_remove()
            self.createPrinterChoices()
        if self.btn1.get() == "3":
            for widget in self.rfrBTNList:
                widget.grid_remove()
            for widget in self.printBTNList:
                widget.grid_remove()
            self.my_button = customtkinter.CTkButton(
                master=self, text="Submit", command=self.submitButton2
            )
            self.my_button.grid(row=8, column=2, sticky="nw")

    def submitButton2(self):
        pass

    def printSubmitBTN(self):
        # print("Printer"+self.btn2.get())
        pass

    def start(self):
        try:
            self.wait_window()
        except Exception as e:
            print(e)
        self.ERI = self.btn1.get()
        self.RFRI = self.btn2.get()
        self.rlm = self.btn3.get()

    def getBtn1(self):
        return self.btn1.get()

    def getBtn2(self):
        return self.btn2.get()

    def getBtn3(self):
        return self.btn3.get()
