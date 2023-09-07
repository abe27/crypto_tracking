# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cryto_tracking(models.Model):
#     _name = 'cryto_tracking.cryto_tracking'
#     _description = 'cryto_tracking.cryto_tracking'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
