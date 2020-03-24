# -*- coding: utf-8 -*-
import itertools
import psycopg2
from odoo.exceptions import except_orm
from odoo import models, fields, api, tools, _

class UpdateTemplate(models.Model):
    _name = "update.product.template"

    product_tmpl_id = fields.Many2one('product.template', string='Product Template')
    product_ids = fields.Many2many('product.template', string='Products')



    @api.model
    def default_get(self, fields_list):
        res = super(UpdateTemplate, self).default_get(fields_list)
        res.update({'product_tmpl_id': self._context.get('active_id', False)})
        return res


    @api.multi
    def update_variants_and_bom(self):

        product_tmpl = self.product_tmpl_id
        bom_id = False

        #build the matrix of all uncreated variants in all products
        all_uncreated_attr_list = self.create_uncreated_attr_combination_matrix()
#       #add all attributes and values of children product to parent product.
        for template in self.product_ids:
            for line in template.attribute_line_ids:
                matching_attr_line = product_tmpl.attribute_line_ids.filtered(lambda attr_line: attr_line.attribute_id == line.attribute_id)
                if matching_attr_line:
                    for value in line.value_ids:
                        if value not in matching_attr_line.value_ids:
                            matching_attr_line.write({'value_ids':[(4, value.id, 0)]})
                else:
                    line.copy(default={'product_tmpl_id':product_tmpl.id})

        #explode to all variants. creates all variants by creating odoos default method
        product_tmpl.create_variant_ids()

        #unlink all unnecessary variants from parent template(unlink unnecessary variants from above created all variants)
        variants_to_unlink = self.env['product.product']
        for product in product_tmpl.product_variant_ids:
            for comb in all_uncreated_attr_list:
                flag = False
                for att in comb:
                    if att not in product.attribute_value_ids:
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

        # finally, create all boms
        if not product_tmpl.bom_ids:
            product_bom_vals = {'product_tmpl_id': product_tmpl.id,
                                'product_qty': 1,
                                'product_uom_id': product_tmpl.uom_id.id,
                                'type': 'normal',
                                }
            bom_id = self.env['mrp.bom'].create(product_bom_vals)
        else:
            bom_id = product_tmpl.bom_ids[0]
        for product in self.product_ids:
            for bom in product.bom_ids:
                bom_line = {}
                for line in bom.bom_line_ids:
                    line.copy(default={'bom_id':bom_id.id})




    def create_uncreated_attr_combination_matrix(self):
        all_uncreated_attr_list = self.get_uncreated_attributes_list(self.product_tmpl_id)
        for templ in self.product_ids:
            all_uncreated_attr_list+=self.get_uncreated_attributes_list(templ)
        return set(all_uncreated_attr_list)




    def get_uncreated_attributes_list(self, template):
        AttributeValues = self.env['product.attribute.value']
        all_attr_combinations = [
            AttributeValues.browse(value_ids)
            for value_ids in itertools.product(*(line.value_ids.ids for line in template.attribute_line_ids if line.value_ids[:1].attribute_id.create_variant))
        ]
        existing_attr_combinations = {frozenset(variant.attribute_value_ids.ids) for variant in template.product_variant_ids}
        uncreated_attr_combinations = [
            value_ids
            for value_ids in all_attr_combinations
            if set(value_ids.ids) not in existing_attr_combinations
        ]
        return uncreated_attr_combinations



UpdateTemplate()
