# -*- coding: utf-8 -*-

{
    "name": "Product Promotions",
    "version": "1.1",
    "author": "Confianz Global",
    "category": 'Sales Management',
    'complexity': "normal",
    "description": """
Allows to promote products based on customer interests.
=======================================================


    """,
    'website': 'http://www.confianzit.com',
    "depends": ['website_sale', 'mrp', 'product','auth_signup'],
    'data': [
              'views/website_template.xml',
              'views/partner_view.xml',
#              'views/product_template.xml',
              'views/product_attributes.xml',
              'security/ir.model.access.csv',
              'data/promo_weekly_cron.xml',
              'data/mail_template.xml',
              'report/report_barcode_template.xml',
              'report/report_template.xml',
             ],
    'demo_xml': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
