from connectpyse.time import time_entries_api
from connectpyse.service import tickets_api,ticket_notes_api, ticket_note,ticket,tickets_api
from rich import print

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from VeritickAPP.doorKey import config

### Connectwise Settings
AUTH=config['cwAUTH']
cwDocumentHeaders = config['cwDocumentHeaders']
tokenHeader = config['cwaHeader']
cwURL = config['cwAPI']['web']
cwAURL = 'https://sca-atl.hostedrmm.com/cwa/api/v1/'


class ticket_search:
    def __init__(self,ticketID):
        self.ticketID = ticketID
        self.address = ''
        self.email = ''   
    
    def getTicketInfo(self):
        gt = tickets_api.TicketsAPI(url=cwURL, auth=AUTH)
        gt.pageSize = 1000
        gt.orderBy = '_info/dateEntered'
        gt = gt.get_ticket_by_id(self.ticketID )
        if gt:
            return gt
            
            # return gt
        return False
        
    def getTimeEntry(self):
        gte = time_entries_api.TimeEntriesAPI(url=cwURL, auth=AUTH)
        gte.conditions = f'chargeToId={self.ticketID}'
        gte.pageSize = 100
        gte.orderBy = 'id desc'
        gte = gte.get_time_entries()
        en = list(gte)
        if en:
            return en
        return False
    
    def getTicketNotes(self):
        ticket_lst=[]
        ticket_notes = ticket_notes_api.TicketNotesAPI(url=cwURL, auth=AUTH, ticket_id=self.ticketID)
        ticket_notes.pageSize = 5
        ticket_notes.orderBy = 'id desc'
        ticket_notes = ticket_notes.get_ticket_notes()
        ls = list(ticket_notes)
        if ls:
            return ls
        return False
       
        


if __name__ == '__main__':  
    ts = ticket_search(326855)
    gt = ts.getTicketNotes()
    print("#########################################")
    for i in gt:
        print(i.text)
        print("#########################################")
    