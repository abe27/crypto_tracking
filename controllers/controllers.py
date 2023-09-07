# -*- coding: utf-8 -*-
# from odoo import http


# class CrytoTracking(http.Controller):
#     @http.route('/cryto_tracking/cryto_tracking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cryto_tracking/cryto_tracking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cryto_tracking.listing', {
#             'root': '/cryto_tracking/cryto_tracking',
#             'objects': http.request.env['cryto_tracking.cryto_tracking'].search([]),
#         })

#     @http.route('/cryto_tracking/cryto_tracking/objects/<model("cryto_tracking.cryto_tracking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cryto_tracking.object', {
#             'object': obj
#         })
