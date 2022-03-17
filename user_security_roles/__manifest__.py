# -*- coding: utf-8 -*-
{
    "name": "User Security Roles",
    "description": """The tool to combine users in roles and to simplify security group assigning""",
    "summary": """ 
    """,
    "version": "15.0.1",
    "category": "Extra Tools",
    "author": "Silverdale",
    "website": "https://wwww.silverdaletech.com",
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users.xml",
        "views/security_role.xml"
    ],


    "application": True,
    "installable": True,
    "auto_install": False,

    "post_init_hook": "post_init_hook",
}