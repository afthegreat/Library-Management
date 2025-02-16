import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days


class LibraryTransaction(Document):

    def before_submit(self):
        """Runs before submitting the transaction document."""
        if self.type == "issue":
            self.validate_issue()

            # Auto-calculate `to_date` based on Library Settings' Loan Period
            loan_period = frappe.db.get_single_value("Library Settings", "Loan_period")  # Ensure correct case
            self.to_date = add_days(self.from_date, loan_period or 30)  # Default to 30 if no value is set

            # Set the book status to "issued"
            book = frappe.get_doc("Book", self.book)
            book.status = "issued"
            book.save()

        elif self.type == "return":
            self.validate_return()

            # Set the book status to "available"
            book = frappe.get_doc("Book", self.book)
            book.status = "available"
            book.save()

    def validate_issue(self):
        """Validates conditions before issuing a book."""
        self.validate_membership()  # Ensure member has a valid membership

        # Get the book document
        book = frappe.get_doc("Book", self.book)

        # Book cannot be issued if it's already issued
        if book.status == "issued":
            frappe.throw("Book is already issued by another member.")


    def validate_membership(self):
        """Checks if the member has an active library membership."""
        active_membership = frappe.get_all(
            "LibraryMembership",
            filters={
                "library_member": self.library_member,
                "docstatus": 1  # 1 means 'Submitted'
            },
            fields=["name", "to_date"]
        )

        if not active_membership:
            frappe.throw("This member does not have an active library membership.")
