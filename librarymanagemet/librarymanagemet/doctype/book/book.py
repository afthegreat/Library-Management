# Copyright (c) 2025, abel and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document
class Book(WebsiteGenerator):

    def before_validate(self):  # Fix: Added 'self' to refer to the current object
        if self.isbn:
            existing_book = frappe.db.exists("Book", {
                "isbn": self.isbn,
                "title": ["!=", self.title]  # Ensure it's not the same book being updated
            })
            if existing_book:
                frappe.throw(
                    title="Duplicate ISBN",
                    msg=f"A book with ISBN {self.isbn} already exists.",
                    exc=frappe.DuplicateEntryError  # Fix: Correct exception handling
                )
