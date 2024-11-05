# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_linked_sale_order_id = fields.Many2one(
        "sale.order", string="Sale", copy=False
    )


