import wx
import wx.grid
from sql_search import *
import better_exceptions; better_exceptions.hook()


dataframe = None

IMAGEFILE = 'sca-logo.jpg'

class Asset:
    value = 0

class MainWindow(wx.Frame,Asset):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        # Search Settings
        panel = wx.Panel(self) 
        my_sizer = wx.BoxSizer(wx.VERTICAL)        

        
      
        ############################ ID Search #####################################
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Search Student')
        my_btn.Bind(wx.EVT_BUTTON, self.id_on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        
        
        ############################ Asset Search ##################################
        self.asset_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.asset_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        asset_my_btn = wx.Button(panel, label='Search Asset')
        asset_my_btn.Bind(wx.EVT_BUTTON, self.asset_on_press)
        my_sizer.Add(asset_my_btn, 0, wx.ALL | wx.CENTER, 5)        
        ###########################################################################
  
        
        # ### New Window Button ###################################################
        # self.new_window_text_ctrl = wx.TextCtrl(panel)
        # my_sizer.Add(self.new_window_text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        # new_window_btn = wx.Button(panel, label='Test Button')
        # new_window_btn.Bind(wx.EVT_BUTTON, self.new_window)
        # my_sizer.Add(new_window_btn, 0, wx.ALL | wx.CENTER, 5)
        ###########################################################################
        
        panel.SetSizer(my_sizer)
        self.CreateStatusBar() # A StatusBar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    
        self.Show(True)
        


    
    def id_on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            p1 = familySearch(value)
            p1.returnAll()
    
    
    def asset_on_press(self, event):
        value = self.asset_text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            assetSearch(value)

    def new_window(self, event):
        value = self.new_window_text_ctrl.GetValue()
        Asset.p = value
        if not value:
            print("You did not enter anything!")
        else:
            secondWindow = MyFrame(value=value)
            secondWindow.Show()



    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Created to make Verification Ticket processing easier\nby keeping the tables in one place.\nCreated by Mark Brown", "About Program", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.




EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'


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

class MyFrame(wx.Frame,Asset):
    """
    Frame that holds all other widgets
    """
    def __init__(self,*args,**kwargs):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "DOWNLOAD HISTORY")
        self._init_gui()
        self.Layout()
        self.Show()

    def _init_gui(self):
        # assign the DataFrame to df
        print(Asset.p)
        dataframe = assetSearch_newWindow(Asset.p)
        print(dataframe)
        table = DataTable(dataframe)

        #declare the grid and assign data
        grid = wx.grid.Grid(self, -1)
        grid.AutoSizeColumns()
        grid.SetTable(table, takeOwnership=True)
        

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


if __name__ == '__main__':  
    app = wx.App(False)
    frame = MainWindow(None, "Verification Process Made Easy")
    app.MainLoop()