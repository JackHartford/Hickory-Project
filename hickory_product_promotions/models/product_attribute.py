# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    is_show_website = fields.Boolean(string="Show in website", default=True)
    is_site = fields.Boolean(string="Is Site Attribute", default=False)
    header_type = fields.Selection([('main', 'Main'), ('sub', 'Sub')], string='Header Type')
