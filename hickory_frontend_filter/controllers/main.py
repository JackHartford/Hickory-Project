# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        """Special route to use website logic in get_combination_info override.
        This route is called in JS by appending _website to the base route.
        """
        response = super(WebsiteSale, self).product(product, category='', search='', **kwargs)
        product_variants = response.qcontext.get('product').product_variant_ids
        prod_variants = []
        if product_variants:
            for p in product_variants:
                variant = {}
                for att in p.attribute_value_ids:
                    v_key = att.attribute_id.name if att.attribute_id else None
                    if v_key:
                        variant[v_key] = att.name
                prod_variants.append(variant)
        response.qcontext.update({
            'prod_variants': prod_variants
        })
        return response
