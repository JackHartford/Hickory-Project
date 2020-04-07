# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'eCommerce Product Attribute Hidden',
    'summary': 'Product Attribute Hidden',
    'sequence': 1001,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.0',
    'author': 'Odoo Inc',
    'description': """
eCommerce Product Attribute Hidden V9 Features
==============================================
* Product Attribute type Hidden V9 Features
    """,
    'category': 'Custom Development',
    'depends': ['sale', 'website_sale'],
    'data': [
        'views/template.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
