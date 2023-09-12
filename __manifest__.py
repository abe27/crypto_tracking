# -*- coding: utf-8 -*-
{
    'name': "Crypto Tracking",

    'summary': """Crypto Tracking System v.1""",

    'description': """Crypto Tracking เป็นระบบที่ใช้สำหรับดูราคา Cryptocurrency จากเว็บ Bitkub, Kucoin และ Binance เพื่อใช้ประกอบการตัดสินใจในการลงทุน""",

    'license': 'Other OSI approved licence',
    'author': "Taweechai Yuenyang",
    "email": "taweechai.yuenyang@outlook.com",
    'website': 'https://abe27.github.io',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/exchange.xml',
        'views/network.xml',
        'views/symbol_group.xml',
        'views/symbol.xml',
        'views/tracking.xml',
        'views/pair.xml',
        'views/transfer_fee.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/symbol_group.xml',
        'demo/exchange.xml',
        'demo/network.xml',
        'demo/currency_pair.xml',
        'demo/symbol.xml',
        'demo/transfer_fee.xml',
    ],
    "application": True,
    'installable': True,  # installable คือ ระบุว่าโมดูลสามารถติดตั้งได้หรือไม่
    'auto_install': False,  # auto_install คือ ระบุว่าโมดูลจะติดตั้งโดยอัตโนมัติหรือไม่
}
