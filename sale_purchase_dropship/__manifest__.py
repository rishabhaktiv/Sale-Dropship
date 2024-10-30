# -*- coding: utf-8 -*-

{
    "name": "Sale Purchase Dropship",
    "version": "17.0.1.0.1",
    "category": "Sale / Purchase",
    "summary": "Manage the dropship functionality for the sale / purchase",
    "description": """
        Sale Purchase Dropship
        ======================================
        This module manage the dropship functionality for the sale / purchase.
    """,
    "author": "Aktiv Software",
    "company": "Aktiv Software",
    "website": "https://www.aktivsoftware.com",
    "depends": ["sale_management", "purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/purchase_order_views.xml",
        "wizard/sale_purchase_wizard_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "LGPL-3",
}
