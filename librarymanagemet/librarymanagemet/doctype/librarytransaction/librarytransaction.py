import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus  # ✅ Import DocStatus

class LibraryTransaction(Document):

    def before_submit(self):
        """Runs before submitting the transaction document."""
        if self.type == "issue":
            self.validate_issue()

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
        self.validate_maximum_limit()  # ✅ Call max limit check

        # Get the book document
        book = frappe.get_doc("Book", self.book)

        # Book cannot be issued if it's already issued
        if book.status == "issued":
            frappe.throw("Book is already issued by another member.")

    def validate_maximum_limit(self):
        """Validates if the member has reached the maximum book issue limit."""
        max_books = frappe.db.get_single_value("LibrarySettings", "maximum_number_of_books")

        # Count the number of issued books for the member
        count = frappe.db.count(
            "LibraryTransaction",  # ✅ Ensure correct Doctype name
            filters={"library_member": self.library_member, "type": "issue", "docstatus": 1}  # ✅ Use `1` instead of `DocStatus.submitted`
        )

        # Check if the limit is exceeded
        if count >= max_books:
            frappe.throw("Maximum limit reached for issuing articles.")

    def validate_membership(self):
        """Checks if the member has an active library membership."""
        active_membership = frappe.get_all(
            "LibraryMembership",  # ✅ Ensure correct Doctype name
            filters={
                "library_member": self.library_member,
                "docstatus": 1  # 1 means 'Submitted'
            },
            fields=["name", "to_date"]
        )

        if not active_membership:
            frappe.throw("This member does not have an active library membership.")
