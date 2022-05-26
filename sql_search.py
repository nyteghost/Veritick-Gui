from pandasgui import show
import pandas as pd
from conn_create import *

conn = open_connection()


def sqlCall(self,queryName,query,variableName):
    queryName= fr"{query} {self.entered_ID}"
    variableName = variable= pd.read_sql(queryName , conn)
    self.variableName = variableName

### Asset Search
def assetSearch_newWindow(assetNumber):
    assetUPSSearch_query = fr"EXEC uspUPSDataByAssetNum {assetNumber}" # Checks Unreturned Equipment in SQL by STID
    # assetUPSSearch = pd.read_sql(assetUPSSearch_query , conn) 
    assetUPSSearch = execute_query(assetUPSSearch_query, parameters=None, conn=None) 
    return assetUPSSearch

class assetSearch:
    def __init__(self, assetNumber):
        self.assetNumber = assetNumber
        self.familyLookupValue = None
        self.currentAssignValue = None

    def assetSearch(self):
        assetUPSSearch_query = fr"EXEC uspUPSDataByAssetNum {self.assetNumber}" # Checks Unreturned Equipment in SQL by STID
        # assetUPSSearch = pd.read_sql(assetUPSSearch_query , conn) 
        assetUPSSearch = execute_query(assetUPSSearch_query, parameters=None, conn=None) 
        show(assetUPSSearch)
    
    def returnAll(self):
        assetUPSSearch_query = fr"EXEC uspUPSDataByAssetNum {self.assetNumber}"
        assetUPSSearch = execute_query(assetUPSSearch_query, parameters=None, conn=None)
        dataset = {
            'Asset UPS Information':assetUPSSearch,
        }
        show(**dataset)


### Family Search    
class familySearch:
    def __init__(self, entered_ID):
        self.entered_ID = entered_ID
        self.familyLookupValue = None
        self.currentAssignValue = None
    
    def familyLookup(self):
        famLookup_query = fr"EXEC uspFamilyLookUp {self.entered_ID}"
        famLookup = pd.read_sql(famLookup_query , conn)
        self.familyLookupValue = famLookup
        return self.familyLookupValue
        
    def currentAssign(self):
        currentAssign_query = fr"EXEC uspFamCurrentAssignByOrgID {self.entered_ID}"
        currentAssign = pd.read_sql(currentAssign_query , conn)
        self.currentAssignValue = currentAssign
    
    def upsData(self):
        upsData_query = fr"EXEC uspUPSDataByAssetNum {self.entered_ID}" # Checks Unreturned Equipment in SQL by STID
        upsData = pd.read_sql(upsData_query , conn)
    
    def unreturned(self):
        unreturned_query = fr"EXEC uspSearchUPSRecordbySTID {self.entered_ID}" # Checks Unreturned Equipment in SQL by STID
        unreturned = pd.read_sql(unreturned_query , conn)   
    
 
        
    def returnAll(self):
        famLookup_query = fr"EXEC uspFamilyLookUp {self.entered_ID}"
        currentAssign_query = fr"uspFamCurrentAssignByOrgID {self.entered_ID}"
        unreturned_query = fr"EXEC [uspFamUnreturnedDevCheck] {self.entered_ID}"# Checks Unreturned Equipment in SQL by STID
        upsData_query = fr"EXEC uspSearchUPSRecordbySTID {self.entered_ID}"  # Checks Unreturned Equipment in SQL by STID
        gopherData_query = fr"EXEC uspGophDataForAssignCBByFam {self.entered_ID}"
    
        # famLookup = pd.read_sql(famLookup_query , conn)
        # currentAssign = pd.read_sql(currentAssign_query , conn)
        # unreturned = pd.read_sql(unreturned_query , conn)  
        # upsData = pd.read_sql(upsData_query , conn)
        # gopherData = pd.read_sql(gopherData_query,conn)
        
        ### Cached ###
        famLookup = execute_query(famLookup_query, parameters=None, conn=None)
        currentAssign = execute_query(currentAssign_query, parameters=None, conn=None)
        unreturned = execute_query(unreturned_query, parameters=None, conn=None)
        upsData = execute_query(upsData_query, parameters=None, conn=None)
        gopherData = execute_query(gopherData_query, parameters=None, conn=None)
        
        dataset = {
            'Family Information':famLookup,
            'Current Assets':currentAssign,
            'UPS Data':upsData,
            'Chrome OS Usage Information for Family': gopherData,
            'Unreturned' : unreturned,
        }
        show(**dataset)


