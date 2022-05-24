import wx
import pandas as pd
from ticket_search import *
from pandasgui import show
import better_exceptions; better_exceptions.hook()
from sql_search import *



class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        # Search Settings
        panel = wx.Panel(self) 
        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        my_btn = wx.Button(panel, label='Search Student')
        my_btn.Bind(wx.EVT_BUTTON, self.id_on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)
        
        # asset_my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.asset_text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.asset_text_ctrl, 0, wx.ALL | wx.EXPAND, 5)        
        asset_my_btn = wx.Button(panel, label='Search Asset')
        asset_my_btn.Bind(wx.EVT_BUTTON, self.asset_on_press)
        my_sizer.Add(asset_my_btn, 0, wx.ALL | wx.CENTER, 5)        
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
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            p1 = familySearch(value)
            p1.returnAll()


    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Created to make Verification Ticket processing easier", "About Program", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.
 
if __name__ == '__main__':  
    app = wx.App(False)
    frame = MainWindow(None, "Verification Process made Easy")
    app.MainLoop()