import pandas as pd

import wx
import wx.grid
from sql_search import *

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'


# data = {
        
#             "titles": ["example123456789", "exampletitle2"],
#             "author": ["author123456", "author2"],
#             "urls": ["https://example.com/", "https://example.com/12345"]
        

# }

data = {
    'Tracking Number': ['1Z4280TT0126337732'], 
    'Reference Number(s)': ['GCA - STUDENT KIT|104330|GCA - STUDENT KIT|104330'], 
    'Status': ['Delivered'], 
    'Manifest Date': ['2019-08-14'], 
    'Ship To Name': ['STUDENT-GEORGIA CYBER ACADEMY'], 
    'Ship To City': ['STOCKBRIDGE'], 
    'Ship To State/Province': ['GA'], 
    'Ship To Country or Territory': ['US'], 
    'Package Reference No# 1': ['GCA - STUDENT KIT'], 
    'Package Reference No# 2': [104330], 
    'Package Reference No# 3': ['nan'], 
    'Package Reference No# 4': ['nan'], 
    'Return To Name': ['nan'], 
    'Ship To Attention': ['NOAH THOMPSON'], 
    'Ship To Address Line 1': ['717 CARRINGTON RIDGE'], 
    'Ship To Address Line 2': ['#717'], 
    'Ship-to Email Address': ['nan'], 
    'Ship To Telephone': [16785938521.0], 
    'Shipment Reference No# 1': ['GCA - STUDENT KIT'], 
    'Shipment Reference No# 2': [104330.0], 
    'New Delivery Attention': ['nan'], 
    'New Delivery Address 1': ['nan'], 
    'New Delivery Address 2': ['nan'], 
    'New Delivery City': ['nan'], 
    'New Delivery Postal Code': ['nan'], 

    
    }


# print(type(data))
# data = assetSearch_newWindow(104330)
# data = data.to_dict('list')
print(type(data))
print(data)




#declare DataTable to hold the wx.grid data to be displayed
class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data
        
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


class MyFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Asset History")
        self._init_gui()
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show()

    def _init_gui(self):
        # assign the DataFrame to df
        df = pd.DataFrame(data)
        table = DataTable(df)
        
        #declare the grid and assign data
        grid = wx.grid.Grid(self, -1,size=(1920,550))
        grid.SetTable(table, takeOwnership=True)
        grid.AutoSizeColumns()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer.Add(grid, 0, wx.EXPAND)


        #add some buttons, and change methods as needed
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancelButton)

        proceedButton = wx.Button(self, wx.ID_OK, "Proceed")
        self.Bind(wx.EVT_BUTTON, self.OnProceed, proceedButton)

        sizerbtns = wx.BoxSizer(wx.HORIZONTAL)
        sizerbtns.Add(cancelButton, 0, wx.CENTER)
        sizerbtns.Add(proceedButton, 0, wx.CENTER)
        
        mainSizer.Add(sizer, 0, wx.ALL, 5)
        mainSizer.Add(sizerbtns, 0, wx.CENTER)
        
        sizer.SetSizeHints(self)
        self.SetSizerAndFit(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.exit)

    def exit(self, event):
        self.Destroy()

    def OnCancel(self, event):
        self.Destroy()
        
    def OnProceed(self, event):
        self.Destroy()

# if __name__ == "__main__":
#     app = wx.App()
#     frame = MyFrame()
#     app.MainLoop()