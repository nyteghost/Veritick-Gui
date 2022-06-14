import pandas as pd
import json
import customtkinter
import tkinter as tk
from tkinter import Text
from ticket_search import conn


def make_config(assetid):
    return {"Company": "GCA", "Argument": assetid}


def assLocJSON(assJSON):
    assetLocationQuery = "EXEC IsolatedSafety.dbo.uspAssetLocationLookup '" + assJSON + "'"
    assetLocation = pd.read_sql(assetLocationQuery, conn)
    return assetLocation


class errorBox(customtkinter.CTkToplevel):
    def __init__(self, titleName, labeltext, populate):
        super().__init__()
        self.titleName = titleName
        self.labeltext = labeltext
        self.populate = populate

        # Main Window
        self.title(f"{titleName}")
        window_width = 450
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create textbox
        textbox = Text(self, height=5, width=52, bg="#292929", fg="silver")

        # Create label
        lbl = customtkinter.CTkLabel(self, text=self.labeltext)
        lbl.config(font=("Courier", 14))

        # Create an Exit button.
        b1 = customtkinter.CTkButton(self, text="Exit", command=self.destroy)

        lbl.pack()
        textbox.pack()
        b1.pack()

        for i in self.populate:
            textbox.insert(tk.END, i+'\n')
        textbox.config(state='disabled')

    def start(self):
        try:
            self.wait_window()
        except Exception as e:
            print(e)


class AssetLoc:
    def __init__(self, stid):
        self.stid = stid
        self.currentAssetsQuery = ('EXEC uspFamCurrentAssignByOrgID ' + self.stid)
        self.currentAssets = pd.read_sql(self.currentAssetsQuery, conn)
        self.currentAssetsList = self.currentAssets['AssetID'].tolist()
        self.locList = []

    def findNone(self):
        for asset in self.currentAssetsList:
            assConfig = make_config(asset)
            assDump = json.dumps(assConfig)
            assLoc = assLocJSON(assDump)
            deviceLoc = assLoc['DeviceLocation'].loc[0]
            containerLoc = assLoc['ContainerLocation'].loc[0]
            if deviceLoc is None and containerLoc is None:
                pass
                # print(f'Both Locations None for {asset}')
                # self.locList.append(f'Both Locations None for {asset}')
            elif deviceLoc is not None:
                print(f'deviceLoc for {asset} is located :{deviceLoc}')
                self.locList.append(f'deviceLoc for {asset} is located :{deviceLoc}')
            elif containerLoc is not None:
                print(f'containerLoc for {asset} is located at :{containerLoc}')
                self.locList.append(f'containerLoc for {asset} is located at :{containerLoc}')
        return self.locList


# STID = '1707390'

# p1 = AssetLoc(STID)
# cacheList = p1.findNone()
# if cacheList:
#     p2 = errorBox('Asset Location', "Asset Location", cacheList)
#     p2.start()
