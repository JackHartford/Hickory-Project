from odoo import models, fields, api, tools, _


class ProductAttributeLine(models.Model):
    _inherit = "product.attribute.line"

    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying on website.')




ProductAttributeLine()
