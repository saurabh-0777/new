{
    'name': 'GYMERP',
    'version': '1.0.0',
    'sequence': 90,
    'summary': 'Track your School pipeline',
    'description': "",
    'website': 'https://www.odoo.com/page/recruitment',
    'depends': [
        'base','sale','account', 'purchase', 'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_info_views.xml',
        'views/product_template_views.xml',
        'views/gym_schedule_info.xml',
        'views/purchase_order_views.xml',
        'views/other_info_views.xml',
        'views/invoice_views.xml',
        # 'views/account_move_views.xml',
        # 'views/account.views.xml',
        'wizard/update_phone_views.xml',


    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}