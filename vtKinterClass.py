import tkinter
from tkinter import *
from PIL import ImageTk, Image
import customtkinter
import sys
import _thread
from veritick import main_run
from customtkinter import CTkToplevel as Toplevel
from customtkinter import CTkLabel as Label
from customtkinter import CTkButton as Button
from customtkinter import CTkFrame
from pandastable import Table, TableModel, config
import os 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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

img_dir = resource_path("images")
                  
img_file = img_dir+"\sca-logo.jpg"


class veriTick(customtkinter.CTk):
    def __init__(self):
        super().__init__()
    
    
        img = ImageTk.PhotoImage(Image.open(img_file))
        self.title("VeriTick")
        self.geometry = (1200,1070)
        self.panel = Label(self, image = img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")

        self.MainFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.MainFrame.pack(pady=20,expand=True)

        self.text_frame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.text_frame.grid(row=2, column=0, padx=10, pady=10)
        self.my_text = Text(self.text_frame, height=20, width=67, wrap=WORD, bd=0, bg="#292929", fg="silver")


        def veritick_on_press():
            value = self.ticketEntry.get().strip()
            switch_state = switch_event()
            if not value:
                print("You didn't enter anything!")
            else:
                print("*******************************************************")
                _thread.start_new_thread(main_run,(value,switch_state))  
                
        def switch_event():
            self.my_text.delete("1.0","end")
            if self.switch_1.get() == 'on':
                switch_state = 1
            else: switch_state = 0
            return switch_state


        self.ticketEntryFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.ticketEntryFrame.grid(row=0, column=0, padx=10, pady=10)

        self.ticketEntry = customtkinter.CTkEntry(self.ticketEntryFrame, width=400, height=40,border_width=1, placeholder_text="Enter Ticket Number",text_color='silver')
        self.ticketEntry.grid(row=0, column=0, padx=10, pady=10)

        self.my_button = customtkinter.CTkButton(self.ticketEntryFrame, text="Lookup", command=veritick_on_press)
        self.my_button.grid(row=0, column=1, padx=10)

        self.switch_frame = customtkinter.CTkFrame(self.MainFrame,corner_radius=10)
        self.switch_frame.grid(row=1, column=0, padx=10, pady=10,sticky='w')
        self.switch_1 = customtkinter.CTkSwitch(self.switch_frame, text="MU Update", command=switch_event,
                                            onvalue="on", offvalue="off",bg_color='#2A2D2E')
        self.switch_1.deselect()
        self.switch_1.pack()

        self.my_text.pack(expand=True)


        def redirector(inputStr):
            self.my_text.insert(INSERT, inputStr)
        sys.stdout.write = redirector
            
    
    def create_toplevel(self):
        window = customtkinter.CTk()
        dFrame = dFrame
        parent = parent
    
        window.attributes('-topmost', 1)
        
        window_width = 1920
        window_height = 200
        
        # get the screen dimension
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        
        window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        window.title('veriTable')
        f = CTkFrame(window)
        f.pack(fill="both",expand=True,padx=20, pady=20)
        # df = TableModel.getSampleData()
        table = pt = Table(f, dataframe=dFrame,
                                showtoolbar=False, showstatusbar=False)
        pt.show()
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)
        pt.show()
        pt.update()
        # print(pt.winfo_reqwidth())
        # print(pt.winfo_reqheight())
    




if __name__ == '__main__':
    app = veriTick()
    app.mainloop()
    # try:
    #     _thread.start_new_thread(root.mainloop(),())
    # except AttributeError as ex:
    #     if str(ex) == "'_tkinter.tkapp' object has no attribute 'root'":
    #         pass