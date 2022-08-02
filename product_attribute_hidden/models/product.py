# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    display_type = fields.Selection(selection_add=[('hidden', 'Hidden')], ondelete={'hidden': 'cascade'})
