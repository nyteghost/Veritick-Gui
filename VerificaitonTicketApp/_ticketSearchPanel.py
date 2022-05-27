import wx
import wx.grid
from sql_search import *
from cw_search import ticket_search
from concurrent import futures
import time
import _thread

import better_exceptions; better_exceptions.hook()
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


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
        self.ticketInfo = wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.EXPAND)        
        self.noteWindow = wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.EXPAND)
        self.timeEntryWindow = wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.EXPAND)
        # redir = RedirectText(self.noteWindow)
        # sys.stdout = redir
        sizer.Add(self.ticketInfo,0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.noteWindow, 0, wx.ALL | wx.EXPAND, 5) 
        sizer.Add(self.timeEntryWindow, 0, wx.ALL | wx.EXPAND, 5) 
    
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
        # cw_ticket_info_btn.Bind(wx.EVT_BUTTON, self.getTicketNotes)
        # cw_ticket_info_btn.Bind(wx.EVT_BUTTON, self.getTimeEntries)
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
            tic = time.time()
            thread_pool_executor.submit(self.blocking_code)
            ts = ticket_search(value)
            gt = ts.getTicketInfo()
            tn = ts.getTicketNotes()
            te = ts.getTimeEntry()
            # index = 0
            # self.ticketInfo.InsertItem(index, gt.id)
            self.ticketInfo.write(str(gt.id)+'\n')
            self.ticketInfo.write(gt.summary+"\n")
            self.ticketInfo.write(gt.status['name'])
            self.noteWindow.write("###################################################################################################################################################################################################################################")
            for i in tn:
                ticket_notes= i.text
                self.noteWindow.write(ticket_notes)
                self.noteWindow.write('\n')
                self.noteWindow.write("###################################################################################################################################################################################################################################")
            
            for i in te:
                ticket_timeEntry = i.notes
                self.timeEntryWindow.write(ticket_timeEntry)
                self.timeEntryWindow.write('\n')
                self.timeEntryWindow.write("###################################################################################################################################################################################################################################")
            toc = time.time()
            print('Done in {:.4f} seconds'.format(toc-tic))
            text.Skip()
    
    def getTicketNotes(self,text):
        value = self.cw_manage_text_ctrl.GetValue().strip()
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            tn = ts.getTicketNotes()
            te = ts.getTimeEntry()
            self.noteWindow.write("###################################################################################################################################################################################################################################")
            for i in tn:
                ticket_notes= i.text
                self.noteWindow.write(ticket_notes)
                self.noteWindow.write('\n')
                self.noteWindow.write("###################################################################################################################################################################################################################################")
            
            for i in te:
                ticket_timeEntry = i.notes
                self.timeEntryWindow.write(ticket_timeEntry)
                self.timeEntryWindow.write('\n')
                self.timeEntryWindow.write("###################################################################################################################################################################################################################################")
            text.Skip()
     
    def getTimeEntries(self,text):
        value = self.cw_manage_text_ctrl.GetValue().strip()
        if not value:
            print("You did not enter anything!")
        else:
            ts = ticket_search(value)
            te = ts.getTimeEntry()
            self.noteWindow.write("###################################################################################################################################################################################################################################")
            for i in te:
                ticket_text = i.notes
                self.timeEntryWindow.write(ticket_text)
                self.timeEntryWindow.write('\n')
                self.timeEntryWindow.write("###################################################################################################################################################################################################################################")
            text.Skip()
    
    def blocking_code(self):
        wx.CallAfter(self.set_label_text, 'running')
  
        for number in range(5):
            wx.CallAfter(self.listbox_insert, str(number))
            time.sleep(1)
  
        wx.CallAfter(self.set_label_text, 'not running')
        
      

     
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