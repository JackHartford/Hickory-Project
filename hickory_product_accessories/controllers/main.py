# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['/product_configurator/set_optional_product_accessory'], type='json', auth="public", methods=['POST'],
                website=True)
    def set_optional_product_accessory(self, attrs, **kw):
        return False
