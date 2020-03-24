{
    'name': 'eCommerce Customization',
    'category': 'Website',
    'sequence': 55,
    'license': 'OEEL-1',
    'summary': 'eCommerce Customization',
    'website': 'https://www.odoo.com/page/e-commerce',
    'version': '1.0',

    'description': """
eCommerce Customization
=======================
this module will bring back functionality of mark as paid button SO

        """,
    'depends': ['website_sale'],
    'data': [
        "views/views.xml",
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
}
