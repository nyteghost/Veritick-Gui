class Default(dict):
    def __missing__(self, key):
        return key


uMAD = """
Thank you for contacting Place regarding your SomeSchool equipment.

Our records indicate {need} assigned to {student_name} {thatwerenot} replaced. 

Has your eligibility changed? If so, please contact your FEL to complete the required forms to update your eligibility.

Otherwise, the following devices need to be returned before a replacement can be sent.

To assist with this, I have added an electronic return label for the following {device} to today's list:
{asset}
The {label} should arrive at your email {email} inbox this afternoon between 3:30 PM and 5:00 PM. In order to print the {label}, you will need to select the yellow "Get Shipping Label" button. From there, you will be taken to a webpage that will give you different options including the ability to print the {label}.

Please note, all other labels on the package MUST be covered or marked out to prevent the package from being returned to you.

If you discover any error in the shipment information, please call us at <Phone Number>, or respond to this email.

Thank you again for allowing us to assist you with your GCA equipment needs.

Best,


"""

por_ticket = """
Hello,

Thank you for contacting Place regarding your SomeSchool equipment. Unfortunately, the address provided at the time that the ticket was placed does not match what we have been provided by GCA as your authorized shipping address.

To complete an address change, please submit the address  along with proof of residency to <Email address>.  Proof of residency can include any of the following documents:
A current and complete Lease Agreement (showing signature date of lease, terms, name and address)
Most recent Mortgage Statement
Most recent Utility Bill showing the service address and issued within 60 days.
The proof of residency documentation must be issued in the Parent/Legal Guardian’s name.  The date must be within the last 60 days.
 
Please note that a cell phone bill is not an acceptable Proof of Residency because it does not have a service address associated with the charge.

If you do not have a Proof of Residency document in your name, an Affidavit of Residence Form may be submitted, completed by you and the home owner/leasee. This form must be notarized.

If you do not have any of the above proof of residency documentation, please contact <Email>, <Phone>

Best, 
 
 """


mu_search = """
SELECT * FROM SomeSchoolAssetMGMT_2_0.Ship.WorldshipData WHERE Label_Method IS NOT NULL AND Date > '{date_to_search}' and Ref2 like '{STID}%'
"""
