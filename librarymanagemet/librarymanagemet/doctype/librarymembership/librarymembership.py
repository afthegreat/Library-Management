import frappe
from frappe.model.document import Document
from frappe.utils import getdate
import frappe.utils

class LibraryMembership(Document):

     def validate(self):
        """Ensure to_date is automatically set based on Loan Period from Library Settings."""
        if not self.from_date:
            frappe.throw("From Date is required.")

        # Convert from_date to a proper date object
        from_date = getdate(self.from_date)

        # Fetch the Loan Period from Library Settings
        loan_period = frappe.db.get_single_value("Library Settings", "Loan period") or 30

        # Automatically set to_date
        self.to_date = add_days(from_date, loan_period)

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
          
         