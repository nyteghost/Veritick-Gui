from tkinter import *
root = Tk()
root.title('Tkinter Apps')
root.resizable(width=TRUE, height=TRUE)
root.geometry('{}x{}'.format(800, 500))

headerbanner=Frame(root,width=790,height=50,bg='khaki')
headerbanner.grid(row=0,column=0,padx=5,pady=2)

bodycontainer=Frame(root,width=790,height=380,bg='tan')
bodycontainer.grid(row=1,column=0,padx=5,pady=0)
bodycontainer.grid_propagate(False) # Stop grid() from resizing bodycontainer

buttoncontainer=Frame(bodycontainer,width=50,height=300,bg='powder blue')
buttoncontainer.grid(row=0,column=0)
buttoncontainer2=Frame(bodycontainer,width=50,height=300,bg='olivedrab1')
buttoncontainer2.grid(row=0,column=1)

root.mainloop()