import wx
import wx.grid
from sql_search import *
from cw_search import ticket_search
from _ticketSearchPanel import TicketWindow
import better_exceptions; better_exceptions.hook()


dataframe = None

IMAGEFILE = 'sca-logo.jpg'

class Asset:
    value = 0
    cwticket = 0

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
  
   
        ### CW Manage Ticket Search ###################################################
        # self.cw_manage_text_ctrl = wx.TextCtrl(panel)
        # my_sizer.Add(self.cw_manage_text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        cw_manage_btn = wx.Button(panel, label='Ticket Search')
        cw_manage_btn.Bind(wx.EVT_BUTTON, self.new_window)
        my_sizer.Add(cw_manage_btn, 0, wx.ALL | wx.CENTER, 5)
        ##########################################################################
        

        
        
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
        # self.SetWindowStyle(wx.STAY_ON_TOP)
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
            p1 = assetSearch(value)
            p1.returnAll()
            

    def new_window(self, event):
        secondWindow = TicketWindow(None, "Verification Process Made Easy")
        secondWindow.Show()
        
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Created to make Verification Ticket processing easier\nby keeping the tables in one place.\nCreated by Mark Brown", "About Program", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

class cw_window(wx.Frame):
    title = "new Window"
    def __init__(self, parent,title):
        wx.Frame.__init__(self, parent, title=title, size=(900,600))
        self.panel=wx.Panel(self, -1)
        my_sizer = wx.BoxSizer(wx.VERTICAL)   
        
        
        
        self.log = wx.TextCtrl(self.panel, -1, size=(400, 500), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        redir = RedirectText(self.log)
        sys.stdout = redir
        

        
        my_sizer.Add(self.log, 0, wx.ALL | wx.EXPAND, 5) 
        # wx.CallLater(10,)
        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()
              
        asset_my_btn = wx.Button(self.panel, label='Ticket Search')
        asset_my_btn.Bind(wx.EVT_BUTTON, self.cw_manage)
        my_sizer.Add(asset_my_btn, 0, wx.ALL | wx.CENTER, 5) 
        
        self.panel.SetSizer(my_sizer)
        self.Show()
    
    def cw_manage(self, event):
        value = Asset.p
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            print(ts.getTimeEntry())
            
    def getcwTimeEntries(self,text):
        value = Asset.p
        ts = ticket_search(value)
        ts.getTimeEntry()
        for timeEntry in ts.getTimeEntry():
            yield timeEntry
      

     
    # def buttonloop(self,event):
    #     os.chdir('d:/KKSC')
    #     dic = getDic()
    #     print dic[0], dic[1], dic[2]
    #     text = tokenize_editor_text(self.control.GetValue())        

    #     try:  ##Exception handler for first occurence(will also cause the list to loop)
    #         print self.wordlist.next()
    #     except:
    #         self.wordlist = getwordlist(text,dic)
    #         print self.wordlist.next()

    # def getwordlist(self,text,dic):
    #     a = []
    #     for word in text:
    #         if word not in dic:
    #             misspelled = word
    #             a.append(misspelled)
    #     for item in a:
    #         yield item


class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


if __name__ == '__main__':  
    app = wx.App(False)
    frame = MainWindow(None, "Verification Process Made Easy")
    app.MainLoop()