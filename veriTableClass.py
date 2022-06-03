from tkinter import *
import customtkinter
from pandastable import Table, TableModel, config

#############################################################################################################################

import os,sys
import sqlalchemy as sa
from sqlalchemy.engine import URL
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from doorKey import config as cfg

### SQL Connection Settings
connection_string = 'Driver={ODBC Driver 17 for SQL Server};''Server='+(cfg['database']['Server'])+';''Database=isolatedsafety;''UID='+(cfg['database']['UID'])+';''PWD='+(cfg['database']['PWD'])+';' 
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
conn = sa.create_engine(connection_url)
rawconn = conn.raw_connection()

unreturned_query = f"EXEC [uspFamUnreturnedDevCheck] " + "147586"  # Checks Unreturned Equipment in SQL by STID
Unreturned = pd.read_sql(unreturned_query , conn)    

dframe = Unreturned

#############################################################################################################################



class tableShow(customtkinter.CTk):
    """Basic test frame for the table"""
    def __init__(self,dFrame, parent=None):
        super().__init__()
        
        def copyTable(*args):
            dFrame.to_clipboard(excel=True, sep=None, index=False, header=None)
        
    

        self.title('veriTable')
        window_width = 1920
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        
        
        ### Table Frame
        f = customtkinter.CTkFrame(self)
        
        # df = TableModel.getSampleData()
        self.table = pt = MyTable(f, 
                                dataframe=dFrame,
                                width = 1920,
                               
                                showtoolbar=False, 
                                showstatusbar=False)
        pt.bind("<Control-c>", self.table.getSelectedRow())
        pt.show()
        
        
        
        #set some options
        options = {'colheadercolor':'green','floatprecision': 5}
        config.apply_options(options, pt)
        pt.autoResizeColumns()
        
        pt.show()
        f.pack(fill='x',expand=True)

        
        
        f.update()
        # print(f.winfo_width())
        # print(f.winfo_height())
        self.geometry(f'{window_width}x{f.winfo_height()+100}+{center_x}+{center_y}')
        self.mainloop()

class MyTable(Table):
    """
      Custom table class inherits from Table.
      This overrides the right click menu.
     """
    def __init__(self, parent=None, app=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        #reference to parent app
        self.app = app
        return

    def popupMenu(self, event, rows=None, cols=None, outside=None):
            """Custom right click menu"""
            popupmenu = Table.popupMenu(event)
            #popupmenu add_command here
            return popupmenu
    
    def copy(self, rows, cols=None):
        """Copy cell contents to clipboard"""
        data = self.getSelectedDataFrame()
        try:
            if len(data) == 1 and len(data.columns)==1:
                data.to_clipboard(index=False,header=False)
            else:
                data.to_clipboard(index=False,header=False)
        except:
            print('Uh-oh')
        return
    

if __name__ == '__main__':
    tableShow(dframe)