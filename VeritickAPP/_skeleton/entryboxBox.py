import customtkinter


class entryBoxMain(customtkinter.CTk):
    def __init__(self, textInput):
        super().__init__()
        self.textInput = textInput
        self.geometry("400x300")
        self.dialog = customtkinter.CTkInputDialog(master=None, text=self.textInput, title="Test")


def entryBox(text):
    entrystart = entryBoxMain(text)
    entry = entrystart.dialog.get_input()
    return entry

if __name__ == "__main__":
    x = entryBox("Test")
    print(x)
    if x == "123":
        print('yes')