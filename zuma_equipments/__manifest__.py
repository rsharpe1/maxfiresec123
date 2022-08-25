# -*- coding: utf-8 -*-
{
    'name': "Equipments",

    'summary': """
        """,

    'description': """
        T30434, T30535, T37023, T37101,44594
    """,

    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",

    'category': 'Helpdesk',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'helpdesk_stock', 'project', 'sale', 'helpdesk_fsm', 'industry_fsm_sale',
                'account', 'sd_base_setup'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/helpdesk_ticket.xml',
        'views/res_config_settings.xml',
        'views/project_task_views.xml',
        'views/sale_order_views.xml',
        'views/account_move.xml',
        'views/sale_portal_template.xml',
        'report/account_reports.xml',
        'report/report_invoice.xml',
        'report/report_saleorder_document.xml',
        'report/report_invoice_document.xml',
        'wizard/product_lot_wizard.xml',
        'views/company_views.xml',
    ],

}
