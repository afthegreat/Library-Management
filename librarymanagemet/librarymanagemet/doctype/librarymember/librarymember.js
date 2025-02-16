// Copyright (c) 2025, abel and contributors
// For license information, please see license.txt

frappe.ui.form.on("LibraryMember", {
    refresh: function (frm) {
        // Create Membership Button
        frm.add_custom_button("Create Membership", function () {
            frappe.new_doc("LibraryMembership", {
                library_member: frm.doc.name
            });
        });

        // Create Transaction Button
        frm.add_custom_button("Create Transaction", function () {
            frappe.new_doc("LibraryTransaction", {
                library_member: frm.doc.name
            });
        });
    },
});

