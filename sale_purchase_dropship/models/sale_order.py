# -*- coding: utf-8 -*-

from odoo import models, _, fields
from odoo import Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_linked_purchase_order_id = fields.Many2one(
        "purchase.order", string="Purchase", copy=False
    )

    def action_confirm(self):
        """Method to update the loyalty points for the partner based on the
        order"""
        if 'wizard' not in self._context:
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
        if 'wizard' in self._context and self._context.get('wizard'):
            res = super().action_confirm()
            return res


