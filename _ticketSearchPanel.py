import wx
import wx.grid
from sql_search import *
from cw_search import ticket_search



import better_exceptions; better_exceptions.hook()

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)
        
        

class TicketWindow(wx.Frame):
    def __init__(self, parent, title):

        super(TicketWindow, self).__init__(parent, title = title, size = (1640,1100))
        self.Centre()
        cw_window(self)
        self.createStatusBar()
        self.createMenu()   

    def createStatusBar(self):
        self.CreateStatusBar() #A Statusbar at the bottom of the window
    
    def createMenu(self):
    
        menu= wx.Menu()
        menuExit = menu.Append(wx.ID_EXIT, "E&xit", "Quit application")

        menuBar = wx.MenuBar()
        menuBar.Append(menu,"&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def OnExit(self, event):
        self.Close(True)   
        
class cw_window(wx.Panel):
    title = "new Window"
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)   
        
        # self.ticketInfo = wx.ListCtrl(
        #     self, 
        #     size = (-1 , - 1),
        #     style=wx.LC_REPORT | wx.BORDER_SUNKEN
        # )
        # self.ticketInfo.InsertColumn(0, 'Ticket Number')
        # self.ticketInfo.InsertColumn(1, 'Summary')
        # self.ticketInfo.InsertColumn(2, 'Status')
        # sizer.Add(self.ticketInfo,0, wx.ALL | wx.EXPAND, 5)
        self.ticketInfo = wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)        
        self.noteWindow = wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY)
        # redir = RedirectText(self.noteWindow)
        # sys.stdout = redir
        sizer.Add(self.ticketInfo,0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.noteWindow, 0, wx.ALL | wx.EXPAND, 5) 
    
        # wx.CallLater(10,)
        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()
              
        # asset_my_btn = wx.Button(panel1, label='Ticket Search')
        # asset_my_btn.Bind(wx.EVT_BUTTON, self.cw_manage)
        # sizer.Add(asset_my_btn, 0, wx.ALL | wx.CENTER, 5) 
        
        ###################### CW Manage Ticket Information #######################
        self.cw_manage_text_ctrl = wx.TextCtrl(self)
        sizer.Add(self.cw_manage_text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        cw_ticket_info_btn = wx.Button(self, label='Search Information')
        cw_ticket_info_btn.Bind(wx.EVT_BUTTON, self.getTicketInfo)
        cw_ticket_info_btn.Bind(wx.EVT_BUTTON, self.getTicketNotes)
        sizer.Add(cw_ticket_info_btn, 0, wx.ALL | wx.CENTER, 5)
        ##########################################################################
       
        # ####################### CW Manage Notes ##################################
        # # self.cw_manage_text_ctrl = wx.TextCtrl(panel1)
        # # sizer.Add(self.cw_manage_text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        # cw_notes_btn = wx.Button(self, label='Ticket Notes')
        # cw_notes_btn.Bind(wx.EVT_BUTTON, self.getTicketNotes)
        # sizer.Add(cw_notes_btn, 0, wx.ALL | wx.CENTER, 5)
        # ##########################################################################
        
        
        
        self.SetSizer(sizer)
        self.Show()
    

    def getTicketInfo(self,text):
        value = self.cw_manage_text_ctrl.GetValue().strip()
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            gt = ts.getTicketInfo()
            # index = 0
            # self.ticketInfo.InsertItem(index, gt.id)
            self.ticketInfo.write(str(gt.id)+'\n')
            self.ticketInfo.write(gt.summary+"\n")
            self.ticketInfo.write(gt.status['name'])
            text.Skip()
     
     
    def getTimeEntries(self,text):
        value = self.cw_manage_text_ctrl.GetValue().strip()
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            ts.getTimeEntry()
            for timeEntry in ts.getTimeEntry():
                yield timeEntry
    
    def getTicketNotes(self,text):
        value = self.cw_manage_text_ctrl.GetValue().strip()
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            tn = ts.getTicketNotes()
            print(len(tn))
            for i in tn:
                ticket_text = i.text
                
                
                self.noteWindow.write(ticket_text)
                self.noteWindow.write('\n')
            text.Skip()
        
      

     
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




if __name__ == '__main__':  
    app = wx.App(False)
    window = TicketWindow(None, "Verification Process Made Easy")
    window.Show()
    app.MainLoop()