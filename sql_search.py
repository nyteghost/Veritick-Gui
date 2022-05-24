from ticket_search import *
from pandasgui import show
import pandas as pd


def sqlCall(self,queryName,query,variableName):
    queryName= fr"{query} {self.entered_ID}"
    variableName = variable= pd.read_sql(queryName , conn)
    self.variableName = variableName


class familySearch:
    def __init__(self, entered_ID):
        self.entered_ID = entered_ID
        self.familyLookupValue = None
        self.currentAssignValue = None
    
    def familyLookup(self):
        famLookup_Query = fr"EXEC uspFamilyLookUp {self.entered_ID}"
        famLookup = pd.read_sql(famLookup_Query , conn)
        self.familyLookupValue = famLookup
        return self.familyLookupValue
        
    def currentAssign(self):
        currentAssign_Query = fr"EXEC uspFamCurrentAssignByOrgID {self.entered_ID}"
        currentAssign = pd.read_sql(currentAssign_Query , conn)
        self.currentAssignValue = currentAssign
    
    def upsData(self):
        upsData_query = fr"EXEC uspUPSDataByAssetNum {self.entered_ID}" # Checks Unreturned Equipment in SQL by STID
        upsData = pd.read_sql(upsData_query , conn)
    
    def unreturned(self):
        unreturned_Query = fr"EXEC uspSearchUPSRecordbySTID {self.entered_ID}" # Checks Unreturned Equipment in SQL by STID
        unreturned = pd.read_sql(unreturned_Query , conn)    
        
    def returnAll(self):
        famLookup_Query = fr"EXEC uspFamilyLookUp {self.entered_ID}"
        famLookup = pd.read_sql(famLookup_Query , conn)
        currentAssign_Query = fr"uspFamCurrentAssignByOrgID {self.entered_ID}"
        currentAssign = pd.read_sql(currentAssign_Query , conn)
        unreturned_Query = fr"EXEC [uspFamUnreturnedDevCheck] {self.entered_ID}"# Checks Unreturned Equipment in SQL by STID
        unreturned = pd.read_sql(unreturned_Query , conn)   
        upsData_query = fr"EXEC uspSearchUPSRecordbySTID {self.entered_ID}"  # Checks Unreturned Equipment in SQL by STID
        upsData = pd.read_sql(upsData_query , conn)
        gopherData_query = fr"EXEC uspGophDataForAssignCBByFam {self.entered_ID}"
        gopherData = pd.read_sql(gopherData_query,conn)
        
        
        dataset = {
            'Family Information':famLookup,
            'Current Assets':currentAssign,
            'UPS Data':upsData,
            'Chrome OS Usage Information for Family': gopherData,
            'Unreturned' : unreturned,
        }
        show(**dataset)


