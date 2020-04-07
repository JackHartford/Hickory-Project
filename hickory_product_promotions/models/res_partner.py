# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    variants_line_ids = fields.One2many('customer.product.variants', 'partner_id', string="Applicable Variants")

    @api.model
    def send_promo_url(self):
        template_id = self.env.ref('product_promotions.email_template_product_promotion')
        customers = self.search([('customer', '=', True), ('variants_line_ids', '!=', False)])
        for customer in customers:
            template_id.send_mail(customer.id, force_send=True)

    @api.multi
    def get_promo_url(self):
        for record in self:
            applicable_product_variants = record.variants_line_ids
            attrib_list_url = []
            attribute_ids = []

            for product in self.env['product.product'].search([('attribute_line_ids', '!=', False)]):
                for attribute in product.attribute_line_ids:
                    if attribute.attribute_id and attribute.attribute_id.id not in attribute_ids:
                        attribute_ids.append(attribute.attribute_id.id)

            for attrib in applicable_product_variants:
                if attrib.attribute.id in attribute_ids:
                    for value in attrib.value_ids:
                        attrib_list_url.append("%s-%s" % (attrib.attribute.id,value.id))
            url = '/shop/?search='
            for val in attrib_list_url:
                url += '&attrib=%s' % (val)
            return url
