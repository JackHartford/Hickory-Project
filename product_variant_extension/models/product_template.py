# -*- coding: utf-8 -*-
import odoo
from odoo import api, fields, models, _
import odoo.addons.web.controllers.main as main
from odoo import http
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = "product.template"
    attribute_condition_ids = fields.One2many('product.attribute.condition', 'product_id', string="Attribute Value Condition")


    @api.multi
    def create_variant_ids(self):
        return True

    @api.multi
    def action_product_variants_create(self):
        self.ensure_one()
        return {
            'name': 'Product Variants to Create',
            'view_mode': 'form',
            'res_model': 'product.variant.create',
            'views': [(self.env.ref('product_variant_extension.product_variant_create_form').id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def add_value_on_variant(self):
        self.ensure_one()
        return {
            'name': 'Add Attribute Values Conditionally',
            'view_mode': 'form',
            'res_model': 'variant.add.value',
            'views': [(self.env.ref('product_variant_extension.variant_add_value_form').id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    _order = 'attribute_id'


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    # add_flag = fields.Boolean("Add/Remove", default=False)
    add_flag = fields.Selection([('add', 'Add All'), ('remove', 'Remove All')], default='remove', string="Add/Remove")
    explode_flag = fields.Boolean(string="Compute with Existing Variants")
    conditional = fields.Boolean(string="Conditional")
    processed = fields.Boolean(string="Processed")

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.conditional:
                attribute_id = self.attribute_id.id
                values = self.value_ids.ids
                records_to_unlink = self.product_tmpl_id.attribute_condition_ids.filtered(
                    lambda val: val.attribute_id.id == attribute_id and val.value_id.id in values)
                records_to_unlink.unlink()
        return super(ProductTemplateAttributeLine, self).unlink()


    @api.multi
    @api.onchange('add_flag')
    def add_remove_values(self):
        for rec in self:
            print('rec.add_flag', rec.add_flag)
            if rec.add_flag == 'add':
                rec.value_ids = [(5, 0, 0), (6, 0, rec.attribute_id.value_ids.ids)]
            else:
                rec.value_ids = [(5, 0, 0)]

    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplateAttributeLine, self).create(vals)
    #     if res.explode_flag:
    #         dup_count = len(res.product_tmpl_id.product_variant_ids)
    #         print('dup_count', dup_count)
    #         value_count = len(res.value_ids)
    #         print('value_count', value_count)
    #
    #         if dup_count > 0 and value_count > 1:
    #             value_ids = res.value_ids.ids
    #             print('value_ids', value_ids)
    #             count = 0
    #             for each in res.product_tmpl_id.product_variant_ids:
    #                 for count in range(value_count-1):
    #                     new_rec = each.copy()
    #                     print('new_rec',new_rec)
    #                     print('count', count)
    #                     new_rec.write({'attribute_value_ids': [(4, value_ids[count])]})
    #                 count +=1
    #                 each.write({'attribute_value_ids': [(4, value_ids[count])]})
    #         elif dup_count > 0 and value_count == 1:
    #             for each in res.product_tmpl_id.product_variant_ids:
    #                 value_ids = res.value_ids.ids
    #                 each.write({'attribute_value_ids': [(4, value_ids[0])]})
    #         else:
    #             pass
    #     return res


ProductTemplateAttributeLine()

class ProductAttributeCondition(models.TransientModel):
    _name = "product.attribute.condition"

    attribute_value_ids = fields.Many2many('product.attribute.value', string='Attribute Values Condition')
    value_id = fields.Many2one('product.attribute.value', string="Values")
    attribute_id = fields.Many2one('product.attribute', string="Attribute")
    add_value_id = fields.Many2one('variant.add.value', string="Add Values")
    product_id = fields.Many2one('product.product', string="Product")
    flg = fields.Boolean(string="flg")


ProductAttributeCondition()
