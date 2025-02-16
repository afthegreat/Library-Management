# Copyright (c) 2025, abel and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Book(Document):

 def before_save(self):
		self.details=f'{self.title} {self.autohor or ""}'


