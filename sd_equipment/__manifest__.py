# -*- coding: utf-8 -*-
{
    'name': "SME Equipments",

    'summary': "Equipment's Tracking on Contact",

    'description': """
        1: Equipment's Tracking on Contact.
       
    """,

    'author': "Silverdale",
    'website': "https://www.silverdale.com",
    'license': 'OPL-1',

    'version': '2209',

    'depends': ['base', 'contacts','stock','sd_base_setup','sd_stock'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'views/res_config_settings.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}