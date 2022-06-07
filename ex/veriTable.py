import customtkinter
from pandastable import Table, TableModel, config
from customtkinter import CTkFrame



def copyTable(dFrame):
    dFrame.to_clipboard(excel=True, sep=None, index=False, header=None)


def tableShow(dFrame, parent=None):
    root = customtkinter.CTk()
    dFrame = dFrame
    parent = parent
 
    root.attributes('-topmost', 1)
    
    window_width = 1920
    window_height = 200
    
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    
    
    
    root.title('veriTable')
    f = CTkFrame(root)
    f.pack(fill="both",expand=True,padx=20, pady=20)
    # df = TableModel.getSampleData()
    table = pt = Table(f, dataframe=dFrame,
                            showtoolbar=False, showstatusbar=False)
    table.autoResizeColumns()
    pt.show()
    
    my_button = customtkinter.CTkButton(root, text="Copy Table", command=copyTable(dFrame))
    my_button.pack()
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    options = {'colheadercolor':'green','floatprecision': 5}
    config.apply_options(options, pt)
    pt.show()
    pt.update()
    # print(pt.winfo_reqwidth())
    # print(pt.winfo_reqheight())
    root.mainloop()

