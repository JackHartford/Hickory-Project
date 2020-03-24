# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.model
    def get_site(self):
        res = ' '
        for attribute in self.attribute_line_ids:
            if attribute.attribute_id.is_site:
                res =  attribute.value_ids and attribute.value_ids[0].name
        return res
