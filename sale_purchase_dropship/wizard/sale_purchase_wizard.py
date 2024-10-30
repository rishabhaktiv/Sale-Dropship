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

    @api.onchange("delivery_date", "vendor_delivery_date")
    def onchage_delivery_date(self):
        """Method to check the date and if the delivery date is past then
         throw a ValidationError exception"""
        if (self.delivery_date and self.delivery_date.date()
                < datetime.now().date() or self.vendor_delivery_date
                and self.vendor_delivery_date.date() < datetime.now().date()):
                raise ValidationError("The date should not be past date")

    def action_confirm(self):
        """ Confirm the given quotation(s) and set their confirmation date.
        If the corresponding setting is enabled, also locks the Sale Order.
        :return: True
        :rtype: bool
        :raise: UserError if trying to confirm cancelled SO's
        """
        if not all(order._can_be_confirmed() for order in self.sale_id):
            raise UserError(
                _(
                    "The following orders are not in a state requiring "
                    "confirmation: %s",
                    ", ".join(self.mapped("display_name")),
                )
            )
        self.sale_id.order_line._validate_analytic_distribution()
        for order in self.sale_id:
            order.validate_taxes_on_sales_order()
            if order.partner_id in order.message_partner_ids:
                continue
            order.message_subscribe([order.partner_id.id])
        self.sale_id.write(self.sale_id._prepare_confirmation_values())
        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of
        # linked records.
        context = self.sale_id._context.copy()
        context.pop("default_name", None)
        self.sale_id.with_context(context)._action_confirm()
        self.sale_id.filtered(lambda so: so._should_be_locked()).action_lock()
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




