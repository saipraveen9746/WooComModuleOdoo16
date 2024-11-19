# -*- coding: utf-8 -*-
{
    'name': 'Febno Construction Module',
    'version': '16.0.1.0',
    'category': 'Account',
    'author': 'Febno',
    'website': "",
    'description': """
        -Construction
    """,
    'depends': ['base','account','project','purchase','stock','purchase_stock'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/project.xml',
        'views/project_sub_menu.xml',
        'views/task_library.xml',
        'views/project_wbs_menu.xml',
        'views/wbs_group_views.xml',
        'views/project_view.xml',
        'views/purchase_requisition_view.xml',
        'views/construction_purchase_order_view.xml',
        'data/labour_lines_squence.xml',
        'data/material_lines_squence.xml',
        'data/purchase_requisition_squence.xml',
        'wizard/wbs_task_wizard.xml',
        'wizard/construction_purchase_order_wizard.xml',
        'wizard/labour_lines_wizard.xml',
        ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}