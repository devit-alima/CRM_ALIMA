# -*- coding: utf-8 -*-
{
    'name': 'crm donateur',
    'description':'CRM ALIMA',
    'version': '1.0',
    'category': 'CRM',
    'depends': [
        'base',
        'mail',
        'document',
    ],
    'author': 'Elimane NDOME, Aliou Samba WELE, ALIMA IT NGO',
    'website': 'alima-ngo.org',
    'license': 'AGPL-3',
    'data': [
        'views/import_don_credit_coop.xml',
        #'views/update_don.xml',
        'views/engagements_view.xml',
        'views/donateur_view.xml',
        'views/dons_view.xml',
        'views/code_media_view.xml',
        'views/menu_view.xml',
        'security/collecte_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
}
