from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_accessory_line_ids = fields.One2many('product.accessory.line', 'product_parent_id', string='Accessory Lines')



class ProductAccessoryLine(models.Model):
    _name = "product.accessory.line"
    _description = "Product Accessory Line"

    product_parent_id = fields.Many2one('product.template', 'Parent product')
    product_id = fields.Many2one('product.template', string='Product', ondelete='cascade', required=True)
    attribute_value_ids = fields.Many2many(
        'product.attribute.value','product_template_accessory_line_rel', string='Apply on Variants')
    is_mandatory = fields.Boolean(string='Is Mandatory')
