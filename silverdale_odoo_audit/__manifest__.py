# -*- coding: utf-8 -*-
{
    'name': "Odoo Audit",

    'summary': """
        Silverdale Odoo Audit Application
    """,

    'description': """
        Silverdale Odoo Audit Application. It audits the custom code and the configuration you did on your odoo intance.
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",
    'version': '14.0.1',
    'category': 'Sale',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/seq.xml',
        'data/ir_config.xml',
        'views/menus.xml',

        'views/odoo_audit_view.xml',
        'views/industry_type_view.xml',
        'views/audit_addons_list.xml',
        'views/master_data_view.xml',

        'reports/report_layout.xml',
        'reports/audit_report.xml',
        'reports/report.xml',

        'wizard/audit_addons_lsit_view.xml',
    ],

    'installable': True,
    'application': True,
}
