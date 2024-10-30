# -*- coding: utf-8 -*-

from odoo import models, _, fields
from odoo import Command


class SaleOrderExtended(models.Model):
    _inherit = "sale.order"

    partner_purchase_order_id = fields.Many2one(
        "purchase.order", string="Purchase", copy=False
    )

    def action_confirm(self):
        """Method to open the wizard"""
        line_list = []
        if self.order_line:
            for line in self.order_line:
                vals = {
                    "product_id": line.product_id.id,
                    "quantity": line.product_uom_qty,
                }
                line_list.append(Command.create(vals))
        context = {
            "default_partner_id": self.partner_id.id,
            "default_sale_id": self.id,
            "default_sale_purchase_wizard_line_ids": line_list,
        }
        return {
            "name": _("Sale Purchase Wizard"),
            "view_mode": "form",
            "res_model": "sale.purchase.wizard",
            "type": "ir.actions.act_window",
            "context": context,
            "target": "new",
        }
