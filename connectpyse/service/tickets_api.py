from ..cw_controller import CWController
# Class for /ticket/tickets
from . import ticket


class TicketsAPI(CWController):
    def __init__(self, **kwargs):
        self.module_url = 'service'
        self.module = 'tickets'
        self._class = ticket.Ticket
        super().__init__(**kwargs)  # instance gets passed to parent object

    def get_tickets(self):
        return super()._get()

    def create_ticket(self, a_ticket):
        return super()._create(a_ticket)

    def get_tickets_count(self):
        return super()._get_count()

    def get_ticket_by_id(self, ticket_id):
        return super()._get_by_id(ticket_id)

    def delete_ticket_by_id(self, ticket_id):
        super()._delete_by_id(ticket_id)

    def replace_ticket(self, ticket_id):
        pass

    def update_ticket_multiple_keys(self, ticket_id, changes_dict):
        return super()._update_multiple_keys(ticket_id, changes_dict)

    def update_ticket(self, ticket_id, key, value):
        return super()._update(ticket_id, key, value)

    def merge_ticket(self, a_ticket, target_ticket_id):
        # return super()._merge(a_ticket, target_ticket_id)
        pass

# get
# create
# count
# search
# getbyid
# delete
# replace
# update
# activities
# count
# timeentries
# count
# scheduleentries
# count
# documents
# count
# products
# count
# configurations
    def create_configurations(self, ticket_id, config_dict):
        # Create Configuration Association
        # /service/tickets/{id}/configurations
        # { id(Integer), deviceIdentifier(String) }
        the_id = '{}/configurations'.format(ticket_id)
        return super()._post_dict(the_id, config_dict)# count
# betbyid
# delete
