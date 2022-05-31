import tkinter
from tkinter import *
import customtkinter
import sys
import _thread
from veritick import main_run
from customtkinter import CTkToplevel as Toplevel
from customtkinter import CTkLabel as Label
from customtkinter import CTkButton as Button


class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Hello World")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

root = customtkinter.CTk()
root.title("VeriTick")
root.geometry = (620,470)
            
def veritick_on_press():
    value = ticketEntry.get().strip()
    switch_state = switch_event()
    if not value:
        print("You didn't enter anything!")
    else:
        _thread.start_new_thread(main_run,(value,switch_state))        

def switch_event():
    print("switch toggled, current value:", switch_1.get())
    if switch_1.get() == 'on':
        switch_state = 1
    else: switch_state = 0
    return switch_state



my_labelframe = customtkinter.CTkFrame(root, corner_radius=10)
my_labelframe.pack(pady=20)

ticketEntry = customtkinter.CTkEntry(my_labelframe, width=400, height=40,border_width=1, placeholder_text="Enter Ticket Number",text_color='silver')
ticketEntry.grid(row=0, column=0, padx=10, pady=10)

my_button = customtkinter.CTkButton(my_labelframe, text="Lookup", command=veritick_on_press)
my_button.grid(row=0, column=1, padx=10)


switch_frame = customtkinter.CTkFrame(root, corner_radius=10)
switch_frame.pack(side=customtkinter.TOP,anchor=NW,pady=10)

switch_1 = customtkinter.CTkSwitch(switch_frame, text="MU Update", command=switch_event,
                                    onvalue="on", offvalue="off",border_width=1)
switch_1.pack(padx=10,pady=10)
switch_1.select()

text_frame = customtkinter.CTkFrame(root, corner_radius=10)
text_frame.pack(pady=10)

my_text = Text(text_frame, height=20, width=67, wrap=WORD, bd=0, bg="#292929", fg="silver")
my_text.pack(pady=10,padx=10)




def redirector(inputStr):
    my_text.insert(INSERT, inputStr)
sys.stdout.write = redirector
    
def create_toplevel(self):
    window = customtkinter.CTkToplevel(self)
    window.geometry("400x200")

    # create label on CTkToplevel window
    label = customtkinter.CTkLabel(window, text="CTkToplevel window")
    label.pack(side="top", fill="both", expand=True, padx=40, pady=40)



    

if __name__ == '__main__':

    root.mainloop()
    try:
        _thread.start_new_thread(root.MainLoop(),())
    except AttributeError as ex:
        if str(ex) == "'_tkinter.tkapp' object has no attribute 'root'":
            pass