from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'





class ProductAccessory(models.Model):
    _name = "product.accessory"
    _description = "Product Accessory"
    _rec_name = 'product_id'


    product_id = fields.Many2one('product.product', required=True, string='Product')
    