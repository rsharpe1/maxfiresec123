# -*- coding: utf-8 -*-
{
    'name': "Maxfire Sales",

    'summary': """
        HTML Order line Note added in sale order
        """,

    'description': """
        1: T45963 - Added Html note field in sale order for order lines in form view, sale order document and portal.
    """,

    "author": "Silverdale",
    "website": "https://www.silverdaletech.com",
    "category": 'Sales',
    "version": '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/sale_views.xml',
        'report/sale_report_templates.xml',
    ],

}
