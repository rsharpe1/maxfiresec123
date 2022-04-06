# -*- coding: utf-8 -*-
{
    "name": "Dymo 4X6 Label",
    'summary': """
        this module will print a label pdf report from product from of size 4X6.
    """,

    'description': """
        Task: 30533,
    """,
    "version": "15.0.0",
    "category": "Extra Tools",
    'author': "Silverdale",
    'website': "http://www.silverdaletech.com",
    'category': 'Product',
    "license": "Other proprietary",

    "depends": [
        "product",
    ],
    "data": [
        'report/product_reports.xml',
        'report/product_product_templates.xml',
        'report/product_template_templates.xml',
        'wizard/product_label_layout_views.xml',
    ],

    "application": True,
    "installable": True,
    "auto_install": False,

    "price": "283.0",
    "currency": "EUR",
}