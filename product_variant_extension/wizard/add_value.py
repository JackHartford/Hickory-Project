# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class AttributeCondition(models.TransientModel):
    _name = "attribute.condition"

    attribute_value_ids = fields.Many2many('product.attribute.value', string='Attribute Values Condition')
    value_id = fields.Many2one('product.attribute.value', string="Values")
    attribute_id = fields.Many2one('product.attribute', string="Attribute")
    add_value_id = fields.Many2one('variant.add.value', string="Add Values")


class VariantAddValue(models.TransientModel):
    _name = "variant.add.value"

    product_id = fields.Many2one('product.template', string="Master Product")
    condition_ids = fields.One2many('attribute.condition', 'add_value_id', string="Value Adding Condition")

    @api.model
    def default_get(self, fields):
        result = super(VariantAddValue, self).default_get(fields)
        result['product_id'] = self._context.get('active_id', False)
        return result

    @api.multi
    def add_value_on_variant(self):
        self.ensure_one()
        product_template = self.env['product.template']
        product_template_ids = product_template.browse(self._context.get('active_ids'))
        for tmpl_id in product_template_ids:
            added_value = {}
            attr_value_ids = []
            existing_attrb = tmpl_id.attribute_line_ids.mapped('attribute_id.id')
            for line in self.condition_ids:
                attr_value_ids.append((0, 0, {
                    'add_value_id': line.add_value_id.id,
                    'value_id': line.value_id.id,
                    'attribute_id': line.attribute_id.id,
                    'flg': False,
                    'attribute_value_ids': [(6, 0, line.attribute_value_ids.ids)],
                }))

                attribute_id = line.value_id.attribute_id.id
                value_id = line.value_id.id
                if attribute_id not in added_value:
                    added_value[attribute_id] = [value_id]
                else:
                    added_value[attribute_id].append(value_id)
            print('added_value---------', added_value)

            new_att_value = []
            for each in added_value:
                if each not in existing_attrb:
                    new_att_value.append((0, 0, {
                        'attribute_id': each,
                        'conditional': True,
                        'value_ids': [(6, 0, added_value[each])],
                    }))
                else:
                    exist_attrb = self.env['product.template.attribute.line'].search(
                        [('attribute_id', '=', each), ('product_tmpl_id', '=', tmpl_id.id)], limit=1)
                    for value in added_value[each]:
                        exist_attrb.write({'value_ids': [(4, value)]})

            tmpl_id.write({'attribute_line_ids': new_att_value,'attribute_condition_ids': attr_value_ids})
        return True


    # @api.multi
    # def add_value_on_variant(self):
    #     self.ensure_one()
    #     Product = self.env["product.product"]
    #     product_template = self.env['product.template']
    #     product_template_ids = product_template.browse(self._context.get('active_ids'))
    #     for tmpl_id in product_template_ids:
    #         added_value = {}
    #         for line in self.condition_ids:
    #             update_variants = []
    #             for variant in tmpl_id.product_variant_ids:
    #                 set1 = set(line.attribute_value_ids.ids)
    #                 set2 = set(variant.attribute_value_ids.ids)
    #                 is_subset = set1.issubset(set2)
    #                 if is_subset:
    #                     update_variants.append(variant.id)
    #             if update_variants:
    #                 prd_rec = Product.browse(update_variants)
    #                 print('prd_rec', prd_rec)
    #                 print('line.value_id.name', line.value_id.name)
    #                 prd_rec.write({'attribute_value_ids': [(4, line.value_id.id)]})
    #                 attribute_id = line.value_id.attribute_id.id
    #                 value_id = line.value_id.id
    #                 if attribute_id not in added_value:
    #                     added_value[attribute_id] = [value_id]
    #                 else:
    #                     added_value[attribute_id].append(value_id)
    #         print('added_value---------', added_value)
    #         new_att_value = []
    #         for each in added_value:
    #             new_att_value.append((0, 0, {
    #                 'attribute_id': each,
    #                 'value_ids': [(6, 0, added_value[each])],
    #             }))
    #         tmpl_id.write({'attribute_line_ids': new_att_value})
    #     return True

