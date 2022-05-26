import re,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from connectpyse.time import time_entries_api
from connectpyse.service import tickets_api
from clint.textui import puts, colored, indent
from loguru import logger
import better_exceptions; better_exceptions.hook()
import re
from fuzzywuzzy import fuzz
import sqlalchemy as sa
from sqlalchemy import exc
from sqlalchemy.engine import URL
import pyodbc
from VeritickAPP.doorKey import config

### SQL Connection Settings
connection_string = 'Driver={ODBC Driver 17 for SQL Server};''Server='+(config['database']['Server'])+';''Database=isolatedsafety;''UID='+(config['database']['UID'])+';''PWD='+(config['database']['PWD'])+';' 
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
conn = sa.create_engine(connection_url)
rawconn = conn.raw_connection()

# Create Cursor
raw_conn = rawconn.cursor()

### Connectwise Settings
AUTH=config['cwAUTH']
cwDocumentHeaders = config['cwDocumentHeaders']
tokenHeader = config['cwaHeader']
cwURL = config['cwAPI']['web']
cwAURL = 'https://sca-atl.hostedrmm.com/cwa/api/v1/'

os.system("")
class style():
    WHITE = '\033[37m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    MAGENTA = '\033[35m'
    BLACK = '\033[30m'
    DARKWHITE =   '\033[0;37m'
    DARKYELLOW= '\033[0;33m'
    DARKGREEN=  '\033[0;32m'
    DARKBLUE=  '\033[0;34m'
    DARKCYAN=   '\033[0;36m'
    DARKRED=   '\033[0;31m'
    DARKMAGENTA='\033[0;35m'
    DARKBLACK =  '\033[0;30m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

@logger.catch
class ticket_search:
    def __init__(self, engineer_notes, shipping_address,email_address):
        debug = 0
        self.debug = debug
        self.en = engineer_notes
        self.address = shipping_address
        self.email = email_address
        
    def find_device(self):
        ticket_summary = self.en.ticket['summary'].lower()
        puts(style.CYAN+"Ticket Summary:"+ticket_summary+style.RESET)
        if 'charger' in ticket_summary:
            device_requested_in_function = 'charger'
            if self.debug == 1:
                logger.debug('Found Charger in ticket_summary.')
            puts('Device Requested:',device_requested_in_function) 
            return device_requested_in_function
        else:
            device_list = ['windows','chromebook','printer','headset','headphone']
            find_device_request = re.compile("Device type(.*)")
            device_request_list = find_device_request.findall(self.en.notes)           
            for device_requested_in_function in device_request_list:
                device_requested_in_function = device_requested_in_function.lower()
                split_res = device_requested_in_function.split()
                res = split_res[-1]
                if res in device_list:
                    if res !='headset':
                        return res
                    else:
                        print('Headphones requested')
                else:
                    return device_requested_in_function
                    

    def find_troubleshooting(self):
        find_troubleshooting = re.compile("Troubleshooting notes:(.*)")
        troubleshooting_list= find_troubleshooting.findall(self.en.notes)
        if not troubleshooting_list:
            if self.debug == 1:
                logger.debug('"Troubleshooting notes:(.*)" did not find anything.')
            find_troubleshooting = re.compile("Troubleshoot steps-(.*)")
            troubleshooting_list= find_troubleshooting.findall(self.en.notes) 
        if troubleshooting_list:
            if self.debug == 1:
                logger.debug("Found Troubleshooting notes with: "+str(find_troubleshooting))
            for troubleshoot in troubleshooting_list:
                return troubleshoot
        else:
            troubleshoot = input("Please enter troubleshooting notes.")
            return troubleshoot
        

    def find_return_label(self):
        label_list = ['ERL','PNM','Email','N/A']
        find_return_label_method = re.compile("Label(.*)")
        return_label_list = find_return_label_method.findall(self.en.notes)
        for rlm in return_label_list:
            rlm = rlm.lower()
            split_res = rlm.split()
            res = split_res[-1]
            mylist = [x for x in res if x in label_list]   
            for i in mylist:
                rlm=i
       
        if not return_label_list:
            manual_rl=input('Please enter Return Label selection from ticket.')
            return_label_list=[manual_rl]           
        
        for rlm in return_label_list:
            res = rlm.split()
            mylist = [x for x in res if x in label_list]
            for rl_in_list in mylist:
                rlm = rl_in_list
            if rlm.strip() == "PNM":
                Label_Method_Decision = "Print Return Label at SCA"
            elif rlm.strip() == "ERL":
                Label_Method_Decision = "Email Electronic Return Label"    
            elif rlm.strip() == "Email":
                Label_Method_Decision = "Email Electronic Return Label"
            elif rlm.strip() == "N/A":
                Label_Method_Decision = ''
            elif 'both' in rlm.strip():
                Label_Method_Decision = 'Both'       
            return Label_Method_Decision

    def compare_shipping_address(self):
        find_ship = re.compile("Shipping Address(.*)")
        shiplist = find_ship.findall(self.en.notes)
        if self.debug == 1:
            logger.debug('"Shipping Address(.*)" did not find anything.')
        if shiplist:
            for sa in shiplist:
                sa = street_name_fix(sa).lower()    
        else:
            if self.debug == 1:
                logger.debug('"Shipping Address(.*)" did not find anything.')
            sa=input('Enter shipping address from note.')
        address_ratio = fuzz.ratio(sa,street_name_fix(self.address).lower())
        # puts("Shipping Address from ticket: "+str(sa)+" "+str(address_ratio)+", match to database entry.")
        return address_ratio, sa
            
    def compare_email_address(self):
        find_email = re.compile("Email:(.*)")
        email_list = find_email.findall(self.en.notes)
        if not email_list:
            logger.debug('"Email:(.*)" did not find anything.')
            find_email = re.compile("LG Email:(.*)")
            email_list = find_email.findall(self.en.notes)
        if not email_list:
            if self.debug == 1:
                logger.debug('"LG Email:(.*)" did not find anything.')
            find_email = re.compile("LG Email(.*)")
            email_list = find_email.findall(self.en.notes)
        if not email_list:
            if self.debug == 1:
                logger.debug('"LG Email(.*)" did not find anything.')
            find_email = re.compile("Email(.*)")
            email_list = find_email.findall(self.en.notes)
        if email_list:
            for ticket_email in email_list:
                ticket_email = ticket_email.strip().lower()
                print("#############################################")
                if "mailto:" in ticket_email:
                    ticket_email=ticket_email.replace('[',"").replace(']',"").replace('(',' ').replace(')',"").replace(':',"")
                    ticket_email = ticket_email.split("mailto",1)[1]
                print(ticket_email)
                print("#############################################")
                database_email = self.email.strip().lower()
            email_Ratio = fuzz.ratio(ticket_email,database_email)
            return email_Ratio,ticket_email


def getShippingInfo(ticketID,Address,LG_Email):
    ### Get Ticket notes from Manage
    engineer_notes = getTickInfo(ticketID)
    if engineer_notes != False:
        return ticket_search(engineer_notes,Address,LG_Email)
    else:
        return False

def testfunction():
    return ticket_search()

   
def street_name_fix(StreetAddress):
    replacements = {'rd': 'road',
                    'cir': 'circle',
                    'dr': 'drive',
                    'ln': 'lane',
                    'ct': 'court',
                    'pl': 'place',
                    'st': 'street',
                    'blvd': 'boulevard',
                    'wy': 'way',
                    'ave':'avenue',
                    'opas':'overpass',
                    'trl':'trail'}
                    
    StreetAddress = StreetAddress.lower().strip().rstrip('.')
    try:
        return '{} {}'.format(' '.join(StreetAddress.split()[:-1]), replacements[StreetAddress.split()[-1]])
    except IndexError:
        return(StreetAddress)
    except KeyError:
        return(StreetAddress)
    



    

@logger.catch
def autoStart(ticketID,debug=''): ## Used for Address-ReturnCheck script to find Tickets for GCA with Scheduled as identifier
    print()
    print('Searching by Ticket Number.')
    gt = tickets_api.TicketsAPI(url=cwURL, auth=AUTH)
    gt.pageSize = 1000
    gt.orderBy = '_info/dateEntered'
    gt = gt.get_ticket_by_id(ticketID)
    if "Return Label" in gt.summary:
        return_label_requested=1
        split_string = gt.summary.split()
        res = [ele for ele in split_string if ele.isnumeric()]
        if len(res)>0:
            STID = res[0]
        else:
            contact_email = gt.contactEmailAddress
            if "@georgiacyber" in contact_email and contact_email != "gcaequipment@georgiacyber.org":
                print('Contact Email:',contact_email)
                split_string = contact_email.split("@", 1)
                STID = split_string[0]
                print('Staff Username:',STID)
            elif contact_email == "gcaequipment@georgiacyber.org":
                raise Exception('Contact is GCAEquipment')
        if debug == 1:
                logger.exception("No STID found in summary.")
    else:
        return_label_requested = 0
        try:
            ticket_contact = gt.contact['name']
            ticket_number = gt.id
            print("Ticket Number :",ticket_number)
            print("Ticket contact:",ticket_contact)
            if True in [char.isdigit() for char in ticket_contact]:
                STID = re.sub("\D","",ticket_contact)
                print('Ticket is for Student.')
            else:
                contact_email = gt.contactEmailAddress
                if "@georgiacyber" in contact_email and contact_email != "gcaequipment@georgiacyber.org":
                    print('Ticket is for Staff.')
                    print('Contact Email:',contact_email)
                    STID = contact_email.replace('@georgiacyber.org',"")
                    print('Staff Username:',STID)
                elif contact_email == "gcaequipment@georgiacyber.org":
                    exit()
        except Exception as e:
            print(e)
            print('No STID found in Contact.')
            if debug == 1:
                logger.exception("No STID found in Contact.")
    return STID,ticketID,return_label_requested


@logger.catch
def getTickInfo(ticketID):
    print()
    gte = time_entries_api.TimeEntriesAPI(url=cwURL, auth=AUTH)
    gte.conditions = f'chargeToId={ticketID}'
    gte.pageSize = 100
    gte.orderBy = 'id desc'
    gte = gte.get_time_entries()
    en = list(gte)
    for i in en:
            ticket_type = str(i)
            if "Return Label Method" in ticket_type or "Student ID" in ticket_type or "Device type" in ticket_type or 'charger in ticket_type':
                return i
    return False