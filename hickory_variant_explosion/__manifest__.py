# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': 'Variant Explosion',
    'category': 'Company Specific',
    'version': '0.0.0',
    'author': 'Blue Stingray',
    'website': 'http://bluestingray.com',

    # |-------------------------------------------------------------------------
    # | Short Summary
    # |-------------------------------------------------------------------------
    # |
    # | Short 1 phrase line / summary of the modules purpose. Used as a subtitle
    # | on module listings.
    # |

    'summary': '',

    # |-------------------------------------------------------------------------
    # | Description
    # |-------------------------------------------------------------------------
    # |
    # | Long description describing the purpose / features of the module.
    # |

    'description': '',

    # |-------------------------------------------------------------------------
    # | Dependencies
    # |-------------------------------------------------------------------------
    # |
    # | References of all modules that this module depends on. If this module
    # | is ever installed or upgrade, it will automatically install any
    # | dependencies as well.
    # |

    'depends': [
        'base',
        'stock',
        'product',
        'purchase',
    ],

    # |-------------------------------------------------------------------------
    # | Data References
    # |-------------------------------------------------------------------------
    # |
    # | References to all XML data that this module relies on. These XML files
    # | are automatically pulled into the system and processed.
    # |

    'data': [
        'security/ir.rule.csv',
        'security/ir.model.access.csv',

        'init.xml',
        'records/asset.xml',
        'records/logging.xml',
        'records/parameter.xml',
        'records/precision.xml',
        'records/property.xml',
        'records/mail/server.xml',
        'records/report/paper_format.xml',
        'records/view/form/form_product_template.xml',
        'records/view/form/form_product_variant_creator.xml',
        'records/view/tree/tree_product_variant_matrix.xml',
        'views/mandatory-products.xml',
        'views/template.xml',
        'views/product_template.xml'
    ],

    # |-------------------------------------------------------------------------
    # | Demo Data
    # |-------------------------------------------------------------------------
    # |
    # | A reference to demo data
    # |

    'demo': ['records/demo/demo.xml', ],

    # |-------------------------------------------------------------------------
    # | Is Installable
    # |-------------------------------------------------------------------------
    # |
    # | Gives the user the option to look at Local Modules and install, upgrade
    # | or uninstall. This seems to be used by most developers as a switch for
    # | modules that are either active / inactive.
    # |

    'installable': True,

    # |-------------------------------------------------------------------------
    # | Auto Install
    # |-------------------------------------------------------------------------
    # |
    # | Lets Odoo know if this module should be automatically installed when
    # | the server is started.
    # |

    'auto_install': False,
}
