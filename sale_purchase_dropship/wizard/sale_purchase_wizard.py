# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class SalePurchaseWizard(models.Model):
    """New Sale Purchase Wizard model"""

    _name = "sale.purchase.wizard"

    partner_id = fields.Many2one("res.partner", string="Partner")
    delivery_date = fields.Datetime("Delivery Date")
    sale_notes = fields.Text("Sales Notes")
    purchase_notes = fields.Text("Purchase Notes")
    vendor_delivery_date = fields.Datetime("Vendor Delivery Date")
    partner_sale_order_id = fields.Many2one("sale.order", string="Sale")
    partner_purchase_order_id = fields.Many2one(
        "purchase.order", string="Purchase"
    )
    sale_purchase_wizard_line_ids = fields.One2many(
        "sale.purchase.wizard.line", "line_id"
    )
    sale_id = fields.Many2one("sale.order", string="Sale")

    @api.onchange('delivery_date', 'vendor_delivery_date')
    def onchage_delivery_date(self):
        """Method to check the date and if the delivery date is past then
         throw a ValidationError exception"""
        if self.delivery_date or self.vendor_delivery_date:
            if (self.delivery_date < datetime.now()
                    or self.vendor_delivery_date < datetime.now()):
                raise ValidationError("The date should not be past date")

    def action_confirm(self):
        self.sale_id.with_context(wizard=True).action_confirm()
        self.sale_id.partner_id = self.partner_id.id
        self.sale_id.partner_purchase_order_id = (
            self.sale_id.order_line.purchase_line_ids.order_id.id
            if (
                    self.sale_id
                    and self.sale_id.order_line
                    and self.sale_id.order_line.purchase_line_ids
                    and self.sale_id.order_line.purchase_line_ids.order_id.id
            )
            else False
        )
        self.sale_id.partner_purchase_order_id.partner_sale_order_id = (
            self.sale_id.id if self.sale_id else False
        )
        self.sale_id.date_order = (
            self.delivery_date if self.delivery_date else False
        )
        self.sale_id.partner_purchase_order_id.date_order = (
            self.vendor_delivery_date if self.delivery_date else False
        )
        return True


class SalePurchaseWizardLine(models.Model):
    """New Sale Purchase Wizard model"""

    _name = "sale.purchase.wizard.line"

    line_id = fields.Many2one("sale.purchase.wizard")
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float("Quantity")





