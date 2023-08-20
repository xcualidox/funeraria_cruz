# -*- coding: utf-8 -*-
# from odoo import http


# class FunerariaCruz(http.Controller):
#     @http.route('/funeraria_cruz/funeraria_cruz/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/funeraria_cruz/funeraria_cruz/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('funeraria_cruz.listing', {
#             'root': '/funeraria_cruz/funeraria_cruz',
#             'objects': http.request.env['funeraria_cruz.funeraria_cruz'].search([]),
#         })

#     @http.route('/funeraria_cruz/funeraria_cruz/objects/<model("funeraria_cruz.funeraria_cruz"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('funeraria_cruz.object', {
#             'object': obj
#         })
