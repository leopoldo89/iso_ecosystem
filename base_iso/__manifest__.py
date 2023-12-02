# -*- coding: utf-8 -*-
{
    'name': "ISO certification 9001, 14001, 45001",
    'summary': "ISO certification 9001, 14001, 45001",
    'description': "ISO certification 9001, 14001, 45001",
    'author': "Piemmeesse srl",
    'website': "https://www.piemmeesee.com/",
    'license': 'LGPL-3',
    'category': 'Tools',
    'version': '16.0.1',
    'depends': ['base','partner_autocomplete', 'contacts', 'hr', 'hr_skills', 'product', 'stock',
                'quality_control', 'partner_manual_rank' ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/base_iso_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_qualification.xml',
        'views/res_partner_satisfaction_views.xml',
        'views/res_partner_supplier_qualification_views.xml',
        'views/employee_qualification_views.xml',
        'views/employee_scheda_valutazione_views.xml',
    ],
    "images": ['static/description/icon.png'],
    "application": True

}
