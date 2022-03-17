# -*- coding: utf-8 -*-
{
    "name": "Send Message Composer",
    "summary": "The tool to always open a full composer on the button 'Send a Message'",
    "description": """
    The tool to always open a full composer on the button 'Send a Message
    """,

    "author": "Silverdale",
    "website": "https://www.silverdaletech.com",
    "category": 'Discuss',
    "version": '15.0.1',

    "depends": ["mail"],
    "data": [
        # "security/ir.model.access.csv",
    ],

    'assets': {
        'web.assets_backend': [
            'sd_mail_compose/static/src/components/chatter/chatter.js',
        ]
    },

    "application": True,
    "installable": True,
    "auto_install": False,
}
