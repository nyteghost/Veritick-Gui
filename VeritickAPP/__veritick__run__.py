import wx
import wx.grid
from veritick import main_run
import better_exceptions; better_exceptions.hook()
import sys
import _thread
import _thread
from wx.lib.expando import ExpandoTextCtrl
import os


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title = title, size = (1640,1100))
        redirectPanel(self)
        
        
        self.Centre()
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
   
    def new_window(self, event):
        secondWindow = MainWindow(None, "Verification Process Made Easy")
        secondWindow.Show()
    
    def ask(parent=None, message='', default_value=''):
        dlg = wx.TextEntryDialog(parent, message, defaultValue=default_value)
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        return result    
      
class redirectPanel(wx.Panel):
    title = "new Window"
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)   
        self.veritick = ExpandoTextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE|wx.TE_READONLY)        
        redir = RedirectText(self.veritick)
        sys.stdout = redir

        sizer.Add(self.veritick,0, wx.ALL | wx.EXPAND, 5)

        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()

        
        ###################### Veritick Submit Button ############$$$$$###########
        self.veritick_text_ctrl = wx.TextCtrl(self)
        self.veritick_text_ctrl.SetHint('Ticket Number')
        sizer.Add(self.veritick_text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        veritick_btn = wx.Button(self, label='Search Information')
        veritick_btn.Bind(wx.EVT_BUTTON, self.veritick_on_press)
        sizer.Add(veritick_btn, 0, wx.ALL | wx.CENTER, 5)
        ##########################################################################


        self.SetSizer(sizer)
        self.Show()
    
    def veritick_on_press(self, event):
        value = self.veritick_text_ctrl.GetValue().strip()
        if not value:
            print("You didn't enter anything!")
        else:
            i = self.veritick.XYToPosition(0, 400)
            self.veritick.Remove(0,i)
            # main_run(value)
            _thread.start_new_thread(main_run,(value,))
    

        




    #here you have your input and you can store it o call a function with it
    
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
    window = MainWindow(None, "Verification Process Made Easy")
    window.Show()
    _thread.start_new_thread(app.MainLoop(),())
    # app.MainLoop()