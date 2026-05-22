# -*- coding: utf-8 -*-
# from odoo import http


# class Discord-manager(http.Controller):
#     @http.route('/discord-manager/discord-manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/discord-manager/discord-manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('discord-manager.listing', {
#             'root': '/discord-manager/discord-manager',
#             'objects': http.request.env['discord-manager.discord-manager'].search([]),
#         })

#     @http.route('/discord-manager/discord-manager/objects/<model("discord-manager.discord-manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('discord-manager.object', {
#             'object': obj
#         })

