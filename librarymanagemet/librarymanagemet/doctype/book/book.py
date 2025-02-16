# Copyright (c) 2025, abel and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class Book(WebsiteGenerator):

 def before_save(self):
		self.details=f'{self.title} {self.autohor or ""}'


