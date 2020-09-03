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
        product_variants = product.product_variant_ids
        prod_variants = {}
        p_prod_variants = []
        if product_variants:
            for p in product_variants:
                variant = {}
                seq_priority_total = 0
                for att in p.attribute_value_ids:
                    v_key = att.attribute_id.name if att.attribute_id else None
                    if v_key:
                        variant[v_key] = att.name
                        seq_priority_total += att.seq_priority
                variant.update({
                    'seq_priority': seq_priority_total
                })
                p_prod_variants.append(variant)
            prod_variants[str(product.id)] = p_prod_variants
            acc_line_ids = product.product_accessory_line_ids
            for ac in acc_line_ids:
                op_prod_variants = []
                op_product_variants = ac.product_id.product_variant_ids
                if op_product_variants:
                    for p in op_product_variants:
                        p_variant = {}
                        for att in p.attribute_value_ids:
                            v_key = att.attribute_id.name if att.attribute_id else None
                            if v_key:
                                p_variant[v_key] = att.name
                        op_prod_variants.append(p_variant)
                    prod_variants[str(ac.product_id.id)] = op_prod_variants

        response.qcontext.update({
            'prod_variants': json.dumps(prod_variants),
            'product': product
        })
        return response

    @http.route(['/product_configurator/get_combination_info_website'], type='json', auth="public", methods=['POST'],
                website=True)
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        response = super(WebsiteSale, self).get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        response.update({
            'is_combination_possible': True
        })
        return response
