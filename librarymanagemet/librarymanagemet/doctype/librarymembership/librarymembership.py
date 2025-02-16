import frappe
from frappe.model.document import Document
from frappe.utils import getdate
import frappe.utils
from frappe.utils import add_days

class LibraryMembership(Document):

     def validate(self):
         """Runs before saving the document to validate dates."""
         from_date = getdate(self.from_date)
         to_date = getdate(self.to_date)

        # Check if to_date is earlier than from_date
         if to_date < from_date:
            frappe.throw("To date is earlier than From date. Please enter the correct date.")


     def before_submit(self):
        # Convert from_date to a datetime.date object
        from_date = getdate(self.from_date)

        # Check if there is already an active membership for this member
        existing_membership = frappe.get_value(
            "LibraryMembership",
            filters={
                "library_member": self.library_member,
                "docstatus": 1,  # Submitted status
            },
            fieldname="name"
        )

        # If an active membership exists, throw an error
        if existing_membership:
            frappe.throw(f"Membership already available for this member: {existing_membership}. No duplicate memberships allowed.")

        def validate(self):
        # Ensure 'from_date' is set
         if not self.from_date:
            frappe.throw("From date is required.")
        
        # Get loan period from Library Settings
        loan_period = frappe.db.get_single_value("LibrarySettings", "loan_period")
        
        if loan_period:
            # Calculate 'to_date' by adding loan_period days to from_date
            self.to_date = add_days(self.from_date, loan_period)
        else:
            frappe.throw("Loan period is not set in Library Settings.")