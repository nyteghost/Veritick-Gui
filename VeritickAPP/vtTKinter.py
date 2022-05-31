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

MainFrame = customtkinter.CTkFrame(root, corner_radius=10)
MainFrame.pack(pady=20)

text_frame = customtkinter.CTkFrame(MainFrame, corner_radius=10)
text_frame.grid(row=2, column=0, padx=10, pady=10)
my_text = Text(text_frame, height=20, width=67, wrap=WORD, bd=0, bg="#292929", fg="silver")


def veritick_on_press():
    value = ticketEntry.get().strip()
    switch_state = switch_event()
    if not value:
        print("You didn't enter anything!")
    else:
        my_text.delete("1.0","end")
        _thread.start_new_thread(main_run,(value,switch_state))  
        
def switch_event():
    my_text.delete("1.0","end")
    print("switch toggled, current value:", switch_1.get())
    if switch_1.get() == 'on':
        switch_state = 1
    else: switch_state = 0
    return switch_state


ticketEntryFrame = customtkinter.CTkFrame(MainFrame, corner_radius=10)
ticketEntryFrame.grid(row=0, column=0, padx=10, pady=10)

ticketEntry = customtkinter.CTkEntry(ticketEntryFrame, width=400, height=40,border_width=1, placeholder_text="Enter Ticket Number",text_color='silver')
ticketEntry.grid(row=0, column=0, padx=10, pady=10)

my_button = customtkinter.CTkButton(ticketEntryFrame, text="Lookup", command=veritick_on_press)
my_button.grid(row=0, column=1, padx=10)

switch_frame = customtkinter.CTkFrame(MainFrame,corner_radius=10)
switch_frame.grid(row=1, column=0, padx=10, pady=10,sticky='w')
switch_1 = customtkinter.CTkSwitch(switch_frame, text="MU Update", command=switch_event,
                                    onvalue="on", offvalue="off",bg_color='#2A2D2E')
switch_1.deselect()
switch_1.pack()




my_text.pack()



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