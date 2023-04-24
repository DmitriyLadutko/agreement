# -*- coding: utf-8 -*-
{
    'name': "Agreement",
    'description': """module for as a test task""",
    'author': "Dima Ladutko",
    'website': "https://www.linkedin.com/in/dmitriy-ladutko-ab7590194/",
    'category': 'Uncategorized',
    'version': '15.0.0.1',
    'depends': ['base', 'mail', ],
    'data': [
        'security/roles.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/sequence.xml',
        'views/agreements_template.xml',
        'views/email.xml',
    ],
    'application': True,
}
