import tkinter
import customtkinter
from customtkinter import CTkToplevel as Toplevel
from customtkinter import CTkLabel as Label
from customtkinter import CTkButton as Button
from customtkinter import CTkFrame

class popUp(customtkinter.CTk):
    def __init__(self,titleName,student):
        super().__init__()        
        self.rfrBTNList=[]
        self.printBTNList=[]
        
        self.student = student
        
        if self.student == 0:
            self.status = 'Student'
        elif self.student == 1:
            self.status = 'Staff'
        
        
        
        self.titleName = titleName
        #### Main Window ###
        self.title(f"{titleName}")
        window_width = 750
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
                # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

       
        self.btn1 = tkinter.StringVar()
        self.btn2 = tkinter.StringVar()


        self.label_radio_group = customtkinter.CTkLabel(master=self,
                                                        text="Please Select Request Equipment:")
        self.label_radio_group.grid(row=0,column=0,sticky='nw')
        
        x = 0
        Equipment_Requested = [f"Replacement {self.status} Kit", f"Replacement {self.status} Printer", "Charger"]
        for i in Equipment_Requested:
            x+=1
            self.radio_button = customtkinter.CTkRadioButton(master=self,
                                                            text= i,
                                                            variable=self.btn1,
                                                            value=x,
                                                            command=self.submitButton)
            self.radio_button.grid(row=x,column=0,sticky='nw')
          
        

        
        # self.my_button = customtkinter.CTkButton(master=self, text="Submit", command=self.submitButton)
        # self.my_button.grid(row=9,column=1,sticky='nw')
        

        
            
    def createRFRBtns(self):
        y=0
        ra=self.label_radio_group2 = customtkinter.CTkLabel(master=self,
                                                        text="Please Select Reason for Return:")
        self.label_radio_group2.grid(row=0,column=2,sticky='nw')
        self.rfrBTNList.append(ra)
        equipment_reason_for_return = ["Display", "OS/MB", "Keyboard", "Camera", "Audio/Mic", "Battery", "Physical Damage"]
        for i in equipment_reason_for_return:
            y+=1
            rb=self.radio_button = customtkinter.CTkRadioButton(master=self,
                                                            text= i,
                                                            variable=self.btn2,
                                                            value=y)
            self.radio_button.grid(row=y,column=2,sticky='nw')
            self.rfrBTNList.append(rb)
            print(rb)
        # self.my_button = customtkinter.CTkButton(master=self, text="Submit", command=self.submitButton2)
        # self.my_button.grid(row=8,column=2,sticky='nw')
            
    def createPrinterChoices(self): 
        y=0
        ra=self.label_radio_group3 = customtkinter.CTkLabel(master=self,
                                                        text="Please Select Reason for Return of Printer:")
        self.label_radio_group3.grid(row=0,column=2,sticky='nw')
        self.printBTNList.append(ra)
        equipment_reason_for_return = ["Hardware", "Software"]
        for i in equipment_reason_for_return:
            y+=1
            rb=self.radio_button = customtkinter.CTkRadioButton(master=self,
                                                            text= i,
                                                            variable=self.btn2,
                                                            value=y,
                                                            command=lambda:print(self.btn2.get()))
            self.radio_button.grid(row=y,column=2,sticky='nw')
            self.printBTNList.append(rb)
            
        self.my_button = customtkinter.CTkButton(master=self, text="Submit", command = self.destroy)
        self.my_button.grid(row=8,column=2,sticky='nw')
        
    def submitButton(self):
        print(self.btn1.get())
        if self.btn1.get()=='1':
            for widget in self.printBTNList:
                widget.grid_remove()
            self.createRFRBtns()
        if self.btn1.get()=='2':
            for widget in self.rfrBTNList:
                widget.grid_remove()
            self.createPrinterChoices()
        if self.btn1.get()=='3':
            for widget in self.rfrBTNList:
                widget.grid_remove()
            self.my_button = customtkinter.CTkButton(master=self, text="Submit", command = self.destroy)
            self.my_button.grid(row=8,column=2,sticky='nw')           
            
    
    def submitButton2(self):
        self.destroy

    
    def printSubmitBTN(self):
        # print("Printer"+self.btn2.get())
        pass
    
    
    def start(self):
        self.mainloop()
        return self.btn1.get(),self.btn2.get()

    


    

