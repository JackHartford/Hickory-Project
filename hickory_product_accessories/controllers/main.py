# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        """Special route to use website logic in get_combination_info override.
        This route is called in JS by appending _website to the base route.
        """
        response = super(WebsiteSale, self).product(product, category='', search='', **kwargs)
        product = response.qcontext.get('product').sudo()
        attrs = []
        attribute_values = product._get_first_possible_combination()
        for av in attribute_values:
            attrs.append({
                'attr': av.attribute_id.name,
                'value': av.name
            })
        optional_product_ids, md_optional_products = self.get_optional_product(attrs, product)
        product.optional_product_ids = [(5, 0, 0)]
        product.optional_product_ids = optional_product_ids
        response.qcontext.update({
            'product': product,
            'md_optional_products': md_optional_products
        })
        return response

    def get_optional_product(self, attribute_values, product_template, **kw):
        product_accessory_line = request.env['product.accessory.line'].sudo()
        accessory_lines = product_accessory_line.search([('product_parent_id', '=', product_template.id)])
        optional_product_ids = []
        mapping_mandatory = []
        if accessory_lines:
            for accessory_line in accessory_lines:
                if accessory_line.attribute_value_ids:
                    if len(accessory_line.attribute_value_ids) <= len(attribute_values):
                        is_all_match = True
                        for av_id in accessory_line.attribute_value_ids:
                            is_match = False
                            for av in attribute_values:
                                if av_id.attribute_id.name == av['attr'] and av_id.name == av['value']:
                                    is_match = True
                            if not is_match:
                                is_all_match = False
                                break
                        if is_all_match:
                            optional_product_ids.append((4, accessory_line.product_id.id))
                            if accessory_line.is_mandatory and not any(accessory_line.product_id.id == m for m in mapping_mandatory):
                                mapping_mandatory.append(accessory_line.product_id.id)
        return optional_product_ids, mapping_mandatory

    @http.route(['/product_configurator/set_optional_product_accessory'], type='json', auth="public", methods=['POST'],
                website=True)
    def set_optional_product_accessory(self, attrs, product_template_id, **kw):
        product_template = request.env['product.template'].sudo()
        if 'context' in kw:
            product_template = product_template.with_context(**kw.get('context'))
        product_template = product_template.browse(int(product_template_id))
        try:
            attribute_values = json.loads(attrs)
            optional_product_ids, md_optional_products = self.get_optional_product(attribute_values, product_template)
            product_template.optional_product_ids = [(5, 0, 0)]
            product_template.optional_product_ids = optional_product_ids
            return md_optional_products
        except ValueError:
            return False
        return False
