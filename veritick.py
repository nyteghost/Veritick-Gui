
from loguru import logger
import xlwings as xw
import better_exceptions; better_exceptions.hook()
import pandas as pd
import numpy as np
import getpass
# from pandasgui import show
import re,os,sys
from doorKey import config
from ticket_search import *
from notes_for_fillin import *
import _thread
import tkinter as tk
from tkinter import ttk
from turtle import textinput
import turtle
from veriTableClass import tableShow

### Settings
better_exceptions.MAX_LENGTH = None
logger.add("./debugger.log", backtrace=True, diagnose=True,rotation="12:00")
debug = 0

def turtletext(boxName,text):
    sc = turtle.Screen()
    sc.bgcolor=(42,45,46)
    sc.setup(0, 0)
    result = textinput(boxName,text)
    sc.bye()  
    if result == '':
        exit()
    return result



# @logger.catch
def main_run(ticketID,switch_state):
    print(ticketID)
    
    print()

    update_master_update = None
    if switch_state == 1:
        update_master_update = 'Y'
    else:
        update_master_update = 'N'
    
    
    
    # update_master_update = 'n'
    if update_master_update == "Y" or update_master_update == "y":
        update_master_updater = 1
        print("Sending to Master Updater Activated")
        print('Opening Master Update excel file.')
        ### Xlwings Settings ###
        localuser = getpass.getuser()
        excel_file = r'C:\Users\{}\Southeastern Computer Associates, LLC\GCA Deployment - Documents\Database\Master Updater.xlsm'.format(localuser)
        wb = xw.Book(excel_file)
        wks = xw.sheets
        # print("Available sheets :\n", wks)
        requestsWS = wks['Requests - Daily']
        returnlabelsWS = wks['IndvReturnLabels']
    elif update_master_update == "N" or update_master_update == "n":
            update_master_updater = 0
            print("Using veriTick for copy and paste ability.")
    elif update_master_update == None:
        exit()      
    else:
        pass    
        
    
    staff = 0
    family_status_dict = {}
    STID = None
    OTN = None
    Company = None
    Contact = None
    Equipment_Requested = None
    Asset_Number = None
    Ship_Method = None
    Reason_For_Return = ''
    Label_For_Returns = ''
    LG_Street1 = None
    LG_Street2 = None
    LG_City = None
    LG_State = None
    LG_Zip = None
    EO = ''
    SDO = None
    DDO = None
    SPECIAL_NOTES = ''
    Label_Method_Decision = None
    troubleshooting_notes = None
    return_label_requested = 0
    withdrawn = None
    # #Pandas Options
    # pd.options.display.max_columns = None
    # pd.options.display.width=None

    ### ID Input Section
    print('\n')
    # ticketID = input(style.BLUE + "Please enter ticket number: "+style.RESET)
    # if ticketID == "X" or ticketID == "x":
    #     pass

    STID,OTN,return_label_requested = autoStart(int(ticketID))
    if STID[0].isdigit() == False:
            findStaffID_query = f"EXEC [staffUserNameToStaffID] " +str(STID) # Checks Unreturned Equipment in SQL by STID
            findStaffID = pd.read_sql(findStaffID_query , conn)
            staff_email = findStaffID['Org_Primary_Email'].loc[0]
            STID = findStaffID['Org_ID'].loc[0]
            print('Staff Email:',staff_email)
            print("Staff Org ID:",STID)
            staff = 1
    elif STID == '':
        pass
    STID = re.sub("[^0-9]", "",STID)              
    print("Performing Verification Check")

    
    # Running Unreturned Query to SQL to check if any unreturned equipment
    unreturned_query = f"EXEC [uspFamUnreturnedDevCheck] " + STID # Checks Unreturned Equipment in SQL by STID
    Unreturned = pd.read_sql(unreturned_query , conn)           
    
    ### Family lookup to retrieve some information needed 
    Fam_Lookup_Query = f"EXEC [uspFamilyLookUp] " + STID
    try:
        Fam_Lookup = pd.read_sql(Fam_Lookup_Query , conn)
        print('Looking up family information.')
        # print(Fam_Lookup)
        if staff == 0:                    
            result = [(x,y) for x,y in zip(Fam_Lookup['StudentID'], Fam_Lookup['EnrollmentStatus'])]
        else:
            result = [(x,y) for x,y in zip(Fam_Lookup['StaffID'], Fam_Lookup['EmploymentStatus'])]
        for x,y in result:
            family_status_dict[x]=y    
    except exc.DBAPIError as e:  
        err_origin = str(e.orig)
        # print(e.statement,"threw an error due to;\n", style.RED+(err_origin)+style.RESET)
        # print(e.args[0])
        qrc = re.search(r"\[([A-Za-z0-9_]+)\]", err_origin)
        if qrc.group(1)== "21000":
            print(style.RED+"Subquery returned more than 1 value. \nThis is not permitted when the subquery follows =, !=, <, <= , >, >= or when the subquery is used as an expression."+style.RESET)
            print('This is usually caused by a user having a ID and another user having the same id but with a Leading 0.')
            print('You will need to run that one manually.')
            logger.exception("Double User found")
        pass
    
    shipmentClearanceQuery = f"EXEC [uspShipmentClearanceCheck] " + str(STID) 
    shipmentClearance = pd.read_sql(shipmentClearanceQuery , conn)

    Kit_Check = shipmentClearance.loc[shipmentClearance['Dev_Option'].str.contains('Kit')]
    Printer_Check = shipmentClearance.loc[shipmentClearance['Dev_Option'].str.contains('Printer')]
    

        #lists
    list_i = []
    list_b = []
    RL_data = []

    #Global Variables
    if staff != 1:
        if len(Fam_Lookup)>=1:
            ContactDF= Fam_Lookup.loc[Fam_Lookup['CW_Contact'].str.contains(STID)]
            ContactDF = ContactDF.reset_index(drop=True)
            try: 
                Contact = ContactDF.loc[0,"CW_Contact"]  
            except Exception as e:
                print("There was a keyError searching for CW_Contact. This is caused by a entering something other than a Student ID. Please verify the Student ID used. ")
                logger.exception("Key Error found when searching for CW_Contact")
                pass
    else:
        Contact = Fam_Lookup['CW_Contact'].loc[0]
    # print("Contact :",Contact)           
    
    if staff == 1:
        LG_Email = Fam_Lookup["StaffEmail"].loc[0]
        FEL_Email = Fam_Lookup["Primary_Email"].loc[0]
        LG_Street1 = Fam_Lookup["Street"].loc[0]
        LG_Street2 = Fam_Lookup["Street2"].loc[0]
        LG_City = Fam_Lookup["City"].loc[0]
        LG_State = Fam_Lookup["State"].loc[0]
        LG_Zip = Fam_Lookup["Zip"].loc[0]
        termDate = Fam_Lookup["Term_Date"].loc[0]

    else:
        LG_Email = Fam_Lookup["LG_Primary_Email"].loc[0]
        FEL_Email = Fam_Lookup["FEL_Email"].loc[0]
        if not FEL_Email:
            FEL_Email = 'None'
        LG_Street1 = Fam_Lookup["LG_Street"].loc[0]
        LG_Street2 = Fam_Lookup["LG_Street2"].loc[0]
        LG_City = Fam_Lookup["LG_City"].loc[0]
        LG_State = Fam_Lookup["LG_State"].loc[0]
        LG_Zip = Fam_Lookup["LG_Zip"].loc[0]
        student_status = Fam_Lookup["EnrollmentStatus"].loc[0]

    Fam_Youngest_Contact = Fam_Lookup["CW_Contact"].loc[0]
    print('Return Label Requested requested '+str(return_label_requested))
    if Unreturned.empty and return_label_requested != 1: #or Check == "Yes":
            Decision = (Kit_Check['Device_Determination']).to_string(index=False)
            if staff == 1:
                Fam_Active = Fam_Lookup.loc[Fam_Lookup['EmploymentStatus'].str.contains('ACTIVE')]
            else:                    
                Fam_Active = Fam_Lookup.loc[Fam_Lookup['EnrollmentStatus'].str.contains('ACTIVE')]
            
            if LG_Street2 == None: 
                Address = LG_Street1 + ' ' + LG_City + ' ' + LG_State + ' ' + LG_Zip
            else:
                Address = LG_Street1 + ' ' + LG_Street2 + ' ' + LG_City + ' ' + LG_State + ' ' + LG_Zip
            
            if Decision == "Cleared For Shipment":
                print(Decision)
                ##Does Address provided match Contact, if not, list together to compare. 
                if staff == 0:
                    print("FEL Email: "+ style.CYAN+FEL_Email+style.RESET)
                    print('LG Email: ' + style.CYAN+str(LG_Email)+style.RESET)
                elif staff ==1:
                    print("Personal Email: "+ style.CYAN+FEL_Email)
                    print('Staff Email: ' + style.CYAN+str(LG_Email)+style.RESET)
                print('Address: '+ style.CYAN+Address+style.RESET)
                
                ERI = 0
                getShipFunc = getShippingInfo(OTN,Address,LG_Email)
                
                if getShipFunc != False:
                    Equipment_Requested = getShipFunc.find_device()
                    if Equipment_Requested == 'charger':
                        ERI = "3"
                        Label_Method_Decision = ''
                    else:
                        if 'hotspot' in Equipment_Requested:
                            print()
                            input(style.RED+'This ticket is asking for assistance with a hot spot. Please forward to Sean.'+style.RESET)
                            pass                            
                        elif 'windows' in Equipment_Requested:
                            print()
                            if staff == 0:
                                print("Student Windows Device Requested.")
                            else:
                                print("Staff Windows Device Requested")
                            input('Press enter to continue')
                        troubleshooting_notes = getShipFunc.find_troubleshooting()
                        Label_Method_Decision = getShipFunc.find_return_label()
                        if Label_Method_Decision == "Both":
                            input('Need to send both  Electric Return Label, and include it box.\nPlease press enter to continue.')
                            Label_Method_Decision = "Email Electronic Return Label"
                        shipping_ratio,ticket_ship_address = getShipFunc.compare_shipping_address()
                        email_Ratio,ticket_email = getShipFunc.compare_email_address()
                        print(style.CYAN+"Device"+style.RESET)
                        print(Equipment_Requested.strip())
                        print()
                        print(style.CYAN+"Troubleshooting Notes"+style.RESET)
                        print(troubleshooting_notes.strip())
                        print()
                        print(style.CYAN+"Return Label Method"+style.RESET)
                        print(Label_Method_Decision)
                        print()

                        if shipping_ratio >=85:
                            print(style.CYAN+"Shipping information "+style.RESET +style.GREEN+str(shipping_ratio)+"%"+style.RESET+" match.")
                            print("Database Ship: "+style.GREEN+str(Address)+style.RESET)
                            print("Ticket Ship: "+style.GREEN+str(ticket_ship_address)+style.RESET)
                        elif  70<= shipping_ratio < 85:
                            print(style.CYAN+"Shipping information "+style.RESET+style.YELLOW+str(shipping_ratio)+"%"+style.RESET+" match.")
                            print("Database Ship "+style.YELLOW+str(Address)+style.RESET)
                            print("Ticket Ship: "+style.YELLOW+str(ticket_ship_address)+style.RESET)
                        else:
                            input('Shipping Address is below the  threshold. Please verify address.')
                            print(style.CYAN+"Shipping information "+style.RESET+style.RED+str(shipping_ratio)+"%"+style.RESET+" match.")
                            print("Database Ship: "+style.RED+str(Address)+style.RESET)
                            print("Ticket Ship: "+style.RED+str(ticket_ship_address)+style.RESET)                            
                        
                        print()
                        
                        if email_Ratio >=85:
                            print(style.CYAN+"Email information "+style.RESET +style.GREEN+str(email_Ratio)+"%"+style.RESET+" match.")
                            print("Database Email: "+style.GREEN+str(LG_Email)+style.RESET)
                            print("Ticket Email: "+style.GREEN+str(ticket_email)+style.RESET)
                        elif  70<= email_Ratio < 85:
                            print(style.CYAN+"Email information "+style.RESET+style.YELLOW+str(email_Ratio)+"%"+style.RESET+" match.")
                            print("Database Email: "+style.YELLOW+str(LG_Email)+style.RESET)
                            print("Ticket Email: "+style.YELLOW+str(ticket_email)+style.RESET)
                        else:
                            input('Email Address is below the  threshold. Please verify email.')
                            print(style.CYAN+"Email information "+style.RESET+style.RED+str(email_Ratio)+"%"+style.RESET+" match.")
                            print("Database Email: "+style.RED+str(LG_Email)+style.RESET)
                            print("Ticket Email: "+style.RED+str(ticket_email)+style.RESET)

                    
                            
                        if staff ==0:
                            if "chromebook" in Equipment_Requested:
                                ERI = "1"
                            elif "printer" in Equipment_Requested:
                                ERI = "2"
                            elif "charger" in Equipment_Requested:
                                ERI = "3"
                            elif "headset" in Equipment_Requested:
                                input('Headset is being requested. Please verify manually.')    
                            
                        elif staff ==1:
                            if "windows" in Equipment_Requested:
                                ERI = "1"
                            elif "printer" in Equipment_Requested:
                                ERI = "2"
                            elif "charger" in Equipment_Requested:
                                ERI = "3"
                            if "headset" in Equipment_Requested:
                                input('Headset Equipment_Requested being requested. Please verify manually.')      
                else:
                    print('No device request information found.\nPlease make your selection below.')
                    if staff == 0:
                        Equipment_Requested = ["1) Replacement Student Kit", "2) Replacement Student Printer", "3) Charger"]
                    elif staff ==1:
                        Equipment_Requested = ["1) Replacement Staff Kit", "2) Replacement Staff Printer", "3) Charger"]
                    # print("\n".join(Equipment_Requested))
                    
                    
                    ERI = turtletext('Equipment Requested',"\n".join(Equipment_Requested))
                    # ERI = 'Please enter the label method requested as it reads exactly in the note.'
                    # rlm = input('Please enter the label method requested as it reads exactly in the note.')
                    
                    rlm = turtletext("Label Requested",'Please enter the label method requested as it reads exactly in the note.')
                    if rlm.strip() == "PNM":
                        Label_Method_Decision = "Print Return Label at SCA"
                    elif rlm.strip() == "ERL":
                        Label_Method_Decision = "Email Electronic Return Label"    
                    elif rlm.strip() == "Email":
                        Label_Method_Decision = "Email Electronic Return Label"   
                
                print()
                if troubleshooting_notes:
                    print("Troubleshooting: "+style.RED+troubleshooting_notes+style.RESET)
                if ERI == 'x':
                    pass   
                elif ERI == "":
                    pass
                elif ERI == "1":
                    if staff == 0:
                        Equipment_Requested = "Replacement Student Kit"
                    elif staff ==1:
                        Equipment_Requested = "Replacement Staff Kit"
                    equipment_reason_for_return = ["1) Display", "2) OS/MB", "3) Keyboard", "4) Camera", "5) Audio/Mic", "6) Battery", "7) Physical Damage"]
                    print(style.BLUE+"Choose Return Reason: "+style.RESET)
                    # print("\n".join(equipment_reason_for_return))
                    # RFRI = input()
                    RFRI = turtletext("Equipment Reason for Return","\n".join(equipment_reason_for_return))
                    if RFRI == "1":
                        Reason_For_Return = "Display Issue"
                    elif RFRI == "2":
                        Reason_For_Return = "OS/MB Issue"
                    elif RFRI == "3":
                        Reason_For_Return = "Keyboard Issue"
                    elif RFRI == "4":
                        Reason_For_Return = "Camera Issue"
                    elif RFRI == "5":
                        Reason_For_Return = "Audio/Mic Issue"
                    elif RFRI == "6":
                        Reason_For_Return = "Battery Issue"
                    elif RFRI == "7":
                        Reason_For_Return = "Physical Damage"
                
                elif ERI == "2" or "printer" in Equipment_Requested:
                    i=0
                    while i < 1: 
                        printCheckVariable = (Printer_Check['Device_Determination']).to_string(index=False)
                        if printCheckVariable == 'Cleared For Shipment':
                            if staff == 0:
                                Equipment_Requested = "Replacement Student Printer"
                            elif staff ==1:
                                Equipment_Requested = "Replacement Student Printer"
                            Printer_Reason_For_Return = ["1) Hardware", "2) Software"]
                            print("Choose Return Reason: ")
                            print("\n".join(Printer_Reason_For_Return))
                            # RFRI = input()
                            RFRI = turtletext("Printer Reason for Return","\n".join(Printer_Reason_For_Return))
                            if RFRI == "1":
                                Reason_For_Return = "Printer Hardware Issue"
                            elif RFRI == "2":
                                Reason_For_Return = "Printer Software Issue"
                            i += 1
                        elif printCheckVariable == "Not Cleared - Not Youngest Enrolled Student in FID":
                            print("Not youngest in family. Searching for youngest.")
                            Contact = Fam_Youngest_Contact
                            print(Contact, "is the youngest in the family.")
                            STID = re.sub('\D','', Contact)
                            shipmentClearanceQuery = f"EXEC uspShipmentClearanceCheck" + ' ' + str(STID) 
                            shipmentClearance = pd.read_sql(shipmentClearanceQuery , conn)
                            Printer_Check = shipmentClearance.loc[shipmentClearance['Dev_Option'].str.contains('Printer')]   
                        else:
                            print(style.RED +printCheckVariable+style.RESET)
                
                elif ERI == "3" or "charger" in Equipment_Requested:
                    Charger_Query = f"EXEC uspFamCurrentAssignByOrgID " + STID
                    Charger_Lookup = pd.read_sql(Charger_Query, conn)
                    Charger_Lookup = Charger_Lookup.loc[Charger_Lookup['STD/STF ID'].str.contains(STID)]
                    Charger_Lookup = Charger_Lookup.loc[Charger_Lookup['Dev_Type'].str.contains('Laptop')]
                    Charger_Lookup.index = range(len(Charger_Lookup.index))
                    model_list = [] 
                    if not Charger_Lookup.empty:
                        if len(Charger_Lookup) == 1:
                            Charger_Model_Number = Charger_Lookup["Model_Number"].loc[0]
                            if Charger_Model_Number == "Chromebook 3400":
                                Equipment_Requested = "Dell 3400 CB Charger"
                            elif Charger_Model_Number == "Chromebook 5400":
                                Equipment_Requested = "Dell 5400 CB Charger"
                            elif Charger_Model_Number == "14e Chromebook":
                                Equipment_Requested = "Lenovo CB Charger"
                            elif Charger_Model_Number == "E550" or "E560" or "E570" or "T440" or "E580":
                                Equipment_Requested = "Lenovo E-Series Charger"
                        elif len(Charger_Lookup) > 1:
                            print("\nThis student has Multiple Laptops. Please select the device they need a charger for.")
                            for i in range(len(Charger_Lookup)):
                                Charger_Model_Number = Charger_Lookup["Model_Number"].loc[i]
                                if Charger_Model_Number == "Chromebook 3400":
                                    Equipment_Requested = "Dell 3400 CB Charger"
                                elif Charger_Model_Number == "Chromebook 5400":
                                    Equipment_Requested = "Dell 5400 CB Charger"
                                elif Charger_Model_Number == "14e Chromebook":
                                    Equipment_Requested = "Lenovo CB Charger"
                                elif Charger_Model_Number == "E550" or "E560" or "E570" or "T440" or "E580":
                                    Equipment_Requested = "Lenovo E-Series Charger"
                                model_list.append(Equipment_Requested)
                                Reason_For_Return = ''
                            for model in model_list:
                                index_count = index_count+1
                                print(index_count , ") " + model)
                            Model_Choice = turtletext("Model Choice","")
            data = {
                'Company': ''
                ,'Contact' : Contact
                ,'Equipment_Requested' : Equipment_Requested
                ,'Asset_Number' : ''
                ,'Ship_Method' : ''
                ,'Reason_For_Return' : [Reason_For_Return]
                ,'Label_For_Returns' : Label_Method_Decision
                ,'Street' : ''
                ,'Street2' : ''
                ,'City' : ''
                ,'State' : ''
                ,'Zip' : ''
                ,'EO' : EO
                ,'OTN' : OTN
                ,'SDO' : ''
                ,'DDO' : ''
                ,'SPECIAL_NOTES' : [SPECIAL_NOTES]
                }
            df = pd.DataFrame(data, columns = [
                'Company'
                ,'Contact'
                ,'Equipment_Requested'
                ,'Asset_Number'
                ,'Ship_Method'
                ,'Reason_For_Return'
                ,'Label_For_Returns'
                ,'Street'
                ,'Street2'
                ,'City'
                ,'State'
                ,'Zip'
                ,'EO'
                ,'OTN'
                ,'SDO'
                ,'DDO'
                ,'SPECIAL_NOTES'
            ])

            if update_master_updater == 1:
                x = None
                while x == None:
                    for row in range(1, 50):
                        if x == None:
                            for col in range(2, 3):
                                if requestsWS.range((row,col)).value == None:
                                    print()
                                    print("The Row is: "+str(row)+" and the column is "+str(col))
                                    x = row
                        else:
                            print("loop ends with",x)
                            break
                        
                # lastRow = requestsWS.range('B' + str(requestsWS.cells.last_cell.row)).end('up').row
                lastRowFill= 'B'+str(row-1)
                lastRowFill2 = str(row-1)
                nRowFill= 'Q'+str(row-1)
                printFilledRow = f"{lastRowFill}:{nRowFill}"
                print(lastRowFill)


                
                df.columns = df.iloc[0] 
                df = df[1:]
                df.head()
                df = df.iloc[: , 1:]
                requestsWS.range("A"+lastRowFill2).value = df
                wb.save()
                val = requestsWS.range(printFilledRow).value
                print(val)
                print()
                
            else:
                tableShow(df)

    else:
        if Unreturned.empty:
            print('Sorry but there are no unreturned equipment. You will need to manually add return labels.')
            pass
            
        if staff == 0:
            print("FEL Email: "+ style.CYAN+FEL_Email+style.RESET)
            print('LG Email: ' + style.CYAN+LG_Email+style.RESET)
            print(style.RED +'This Family has Outstanding Equipment'+style.RESET)
        elif staff ==1:
            print("Personal Email: "+ style.CYAN+FEL_Email+style.RESET)
            print('Staff Email: ' + style.CYAN+str(LG_Email)+style.RESET)
            print(style.RED +'This Staff member has Outstanding Equipment'+style.RESET)
        Unreturned_New = Unreturned[['AssetID', 'Dev_Cat', 'Model_Number','AssignDate','CW_Contact']].copy()
        print(Unreturned_New)
        print('\n')

        #Creation of Dataframe
        columns = [
                'Contact'
                ,'Equipment Being Returned'
                ,'Reason For Return'
                ,'Labels For Returns'
            ]
        df = pd.DataFrame(columns = columns)
        df1 = pd.DataFrame(columns = columns)
        list_c=[]
        new_list_b=[]
        for index, row in Unreturned.T.iteritems():#iterates over the unreturned equipment
            list_b.append(row.FERPA_Contact)
            list_c.append(row.Dev_Cat +' '+ row.Model_Number + " GCA-"+str(row.AssetID))
            
            ### Checks if student is withdrawn
            for i in list_b:
                if staff == 0:
                    y = int(re.sub("[^0-9]", "",i))
                    for k,v in family_status_dict.items():
                        if k == y:
                            if v == "WITHDRAWN":
                                if k != STID:
                                    withdrawn = 'sibling'
                                    new_list_b.append(k)
                                    values = [row.CW_Contact, row.Dev_Cat,'Withdrawn','Email Electronic Return Label']
                                else:
                                    withdrawn = True
                                    new_list_b.append(k)
                                    values = [row.CW_Contact, row.Dev_Cat,'Withdrawn','Email Electronic Return Label']
                            else:
                                values = [row.CW_Contact, row.Dev_Cat,'Normal Return','Email Electronic Return Label']
                else:
                    for k,v in family_status_dict.items():
                            if v == "ACTIVE":
                                new_list_b.append(k)
                                values = [row.CW_Contact, row.Dev_Cat,'Normal Return','Email Electronic Return Label']
                            else:
                                values = [row.CW_Contact, row.Dev_Cat,'Withdrawn','Email Electronic Return Label']
                
            ### CHANGES THE RESULTS OF UNRETURNED INTO A LIST. THEN FROM LIST TO NUMPY ARRAY WHICH IS THEN APPENDED TO A DATAFRAME.
            # values = [row.CW_Contact, row.Dev_Cat,'Normal Return','Email Electronic Return Label']
            values = np.array(values)
            values = np.where(values == 'Hotspot','GCA Hotspot', values)
            if staff == 0:
                values = np.where(values == 'Printer','Student Printer', values)
                values = np.where(values == 'Kit','Student Kit', values)
            elif  staff == 1:
                values = np.where(values == 'Printer','Staff Printer', values)
                values = np.where(values == 'Kit','Staff Kit', values)
            zipped = zip(columns,values)
            a_dictionary = dict(zipped)
            RL_data.append(a_dictionary)
        df1 = pd.DataFrame.from_dict(RL_data)
        df1['IS_DUPLICATED']= df1.duplicated(subset=["Contact","Reason For Return"])
        for index,row in df1.iterrows():
            if row['Reason For Return'] == 'Withdrawn':
                if row['IS_DUPLICATED'] == True:
                    df1.at[index,'Equipment Being Returned']='ES - ALL'
                    df1 = df1.drop_duplicates(subset=["Contact","Reason For Return"], keep='last')
        df1 = df1.drop('IS_DUPLICATED', axis=1)
        df1=df1.reset_index(drop=True)

        if update_master_updater == 1:
            x = None
            while x == None:
                for row in range(1, 50):
                    if x == None:
                        for col in range(2, 3):
                            if returnlabelsWS.range((row,col)).value == None:
                                print("The Row is: "+str(row)+" and the column is "+str(col))
                                x = row
                    else:
                        print("loop ends with",x)
                        break
                    
            lastRowFill= 'B'+str(row-1)
            lastRowFill2 = str(row-1)
            nRowFill= 'L'+str(row-1)
            printFilledRow = f"{lastRowFill}:{nRowFill}"
            print(lastRowFill)
            # val = returnlabelsWS.range(lastRowFill).value
            df1.columns = df1.iloc[0] 
            df1 = df1[1:]
            df1.head()
            returnlabelsWS.range("A"+lastRowFill2).value = df1
            wb.save()
            val = returnlabelsWS.range(printFilledRow).value
        else:
            if df1.empty:
                print('Sorry but there are no unreturned equipment. You will need to manually add them.')
                pass
            tableShow(df1)

                
        print()
        print("Return label requested: "+str(return_label_requested))
        if return_label_requested == 0:
            print(style.RED +', '.join(list_b)+style.RESET)
            print()
            print(style.RED +'\n'.join(list_c)+style.RESET)
            if len(list_b) >1:
                student_list= ",".join(list_b[:-1]) +"& "+list_b[-1]
                deviceamount = 'devices'
                labelamount = 'labels'
                need = 'there are devices'
                thatwerenot = "that were not returned after they were"

            else:
                student_list= ",".join(list_b[:-1]) +""+list_b[-1]
                deviceamount = 'device'
                labelamount = 'label'
                need = 'a device is'
                thatwerenot = "that was not returned after it was"
            asset_list = "\n".join(list_c)

            if withdrawn != True:
                uMADFormat = uMAD.format_map(Default(need = need,thatwerenot=thatwerenot,device=deviceamount,label=labelamount,email=LG_Email,student_name=student_list,asset=asset_list))
                print('\n',uMADFormat)
                if Label_Method_Decision == "Print Return Label at SCA":
                    print(style.WHITE+'Choose "Shipping - Replacement PRL" as note to send.'+style.RESET)
                    print('Also let Warehouse know!')
                    print(f"@Shipping\n{Contact}\nPrint at warehouse, include in box")
                elif Label_Method_Decision == "Email Electronic Return Label":
                    print(style.WHITE+'Choose "Shipping - Replacement ERL" as note to send.'+style.RESET)
                print('\n')
            else:
                print(style.WHITE+'Choose "Shipping - Replacement ERL" as note to send.'+style.RESET)
        # except Exception as e:
        #     print(e)
        #     print('Issue with Outstanding DataFrame Creation')
    print('Done')





if __name__ == '__main__': 
    main_run(365891)