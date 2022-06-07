import tkinter
r = tkinter.Tk()
age = '''
O.o
    giga
'''
gage = 'vrum'
r.title("getherefast")

def gtc(dtxt):
    r.clipboard_clear()
    r.clipboard_append(dtxt)

tkinter.Button(text='age', command=lambda: gtc(age)).grid(column=1, row=0)
tkinter.Button(text='gage', command=lambda: gtc(gage)).grid(column=2, row=0)

r.mainloop()