# -*- coding: utf-8 -*-

{
    "name": "Product Accessories",
    "version": "1.0",
    "author": "Novobi LLC",
    "category": 'Product Accessory',
    'complexity': "normal",
    "description": """
Allows to add accessories (mandatory/optional) to products.
=======================================================


    """,
    'website': 'http://www.novobi.com',
    "depends": ['stock', 'product'],
    'data': [
                'security/ir.model.access.csv',
                'views/assets.xml',
                'views/product_accessories_views.xml'
             ],
    'demo_xml': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}