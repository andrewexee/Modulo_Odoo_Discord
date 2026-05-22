# -*- coding: utf-8 -*-
{
    'name': "Discord Manager",
    'summary': "Gestión de servidores, canales, webhooks y mensajes de Discord desde Odoo",
    'description': """
Gestión de Discord para registrar servidores, canales, webhooks y mensajes.
Permite mantener un histórico de envíos y administrar la configuración desde Odoo.
""",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Tools',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/discord_security.xml',
        'security/ir.model.access.csv',
        'views/discord_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}

