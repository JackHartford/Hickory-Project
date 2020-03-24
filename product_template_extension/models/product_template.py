# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
import itertools
import psycopg2
from odoo.exceptions import except_orm

class ProductTemplate(models.Model):

    _inherit = 'product.template'



    bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', 'Bill of Materials', copy=True)
    # attribute_line_ids = fields.One2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes', copy=True)




    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new_template = super(ProductTemplate, self).copy(default)
        existing_attr_combinations = [variant.attribute_value_ids for variant in self.product_variant_ids]
        variants_to_unlink = self.env['product.product']
        for product in new_template.product_variant_ids:
            flag = False
            for comb in existing_attr_combinations:
                if all([c.id in product.attribute_value_ids.ids for c in comb]):
                    flag = True
                    break
            if not flag:
                variants_to_unlink |= product
        # unlink or inactive product
        for variant in variants_to_unlink:
            try:
                with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                    variant.unlink()
            # We catch all kind of exception to be sure that the operation doesn't fail.
            except (psycopg2.Error, except_orm):
                variant.write({'active': False})
                pass

        return new_template




    @api.multi
    def create_variant_ids(self):

        existing_attr_combinations = [variant.attribute_value_ids for variant in self.product_variant_ids]
        res = super(ProductTemplate, self).create_variant_ids()

        #unlink all unnecessary variants from parent template(unlink unnecessary variants from above created all variants)
        if existing_attr_combinations:
            variants_to_unlink = self.env['product.product']
            for product in self.product_variant_ids:
                flag = False
                for comb in existing_attr_combinations:
                    if all([c.id in product.attribute_value_ids.ids for c in comb]):
                        flag = True
                        break
                if not flag:
                    variants_to_unlink |= product
            # unlink or inactive product
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation doesn't fail.
                except (psycopg2.Error, except_orm):
                    variant.write({'active': False})
                    pass
        return res





ProductTemplate()
