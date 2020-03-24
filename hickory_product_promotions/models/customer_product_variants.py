# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductVariants(models.Model):
    _name = 'customer.product.variants'

    attribute = fields.Many2one('product.attribute', string="Attribute")
    value_ids = fields.Many2many('product.attribute.value', 'product_promo_rel', 'product_id')
    partner_id = fields.Many2one('res.partner', string="Customer")
