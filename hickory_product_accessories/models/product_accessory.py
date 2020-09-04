from odoo import fields,api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_accessory_line_ids = fields.One2many('product.accessory.line', 'product_parent_id', string='Accessory Lines')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    priority = fields.Integer(string='Priority')

    @api.model
    def cal_priority(self):
        all_products = self.env['product.product'].search([])
        if all_products:
            for p in all_products:
                if p.attribute_value_ids and len(p.attribute_value_ids) > 0:
                    priority = sum([av.seq_priority for av in p.attribute_value_ids])
                    p.write({
                        'priority': priority
                    })
        return True

class ProductAccessoryLine(models.Model):
    _name = "product.accessory.line"
    _description = "Product Accessory Line"

    product_parent_id = fields.Many2one('product.template', 'Parent product')
    product_id = fields.Many2one('product.template', string='Product', ondelete='cascade', required=True)
    valid_product_attribute_value_wnva_ids = fields.Many2many('product.attribute.value',
                                                              related='product_parent_id.valid_product_attribute_value_wnva_ids')
    attribute_value_ids = fields.Many2many(
        'product.attribute.value','product_template_accessory_line_rel', string='Apply on Variants')
    is_mandatory = fields.Boolean(string='Is Mandatory')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    seq_priority = fields.Integer('Order')

    def write(self, vals):
        res = super(ProductAttributeValue, self).write(vals)
        seq = vals.get('sequence')
        if seq and self.attribute_id.id:
            attr_values = self.search([('attribute_id', '=', self.attribute_id.id)])
            if attr_values and len(attr_values) > 0:
                seq_priority = 0
                for attr in attr_values:
                    attr.write({
                        'seq_priority': seq_priority
                    })
                    seq_priority += 1
        return res

    @api.model
    def create(self, vals):
        attr_id = vals.get('attribute_id')
        if attr_id:
            max_seq_priority = max(self.search([('attribute_id', '=', attr_id)]).mapped('seq_priority'))
            if max_seq_priority and max_seq_priority > 0:
                vals.update({
                    'seq_priority': max_seq_priority + 1
                })
        res = super(ProductAttributeValue, self).write(vals)
        return res

    @api.model
    def cal_priority(self):
        return True
