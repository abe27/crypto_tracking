# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

class exchange_list(models.Model):
    _name = 'cryto_tracking.exchange_list'
    _description = 'รายชื่อ Exchange'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(size=150, string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    api_key = fields.Text(string="API Key", required=True, tracking=True)
    api_secret = fields.Text(string="API Secret", required=True, tracking=True)
    api_passphrase = fields.Text(string="API Passphrase", tracking=True)
    exchange_logo = fields.Image(string="Logo", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class symbol_group(models.Model):
    _name = 'cryto_tracking.symbol_group'
    _description = 'ประเภท'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(size=150, string="Group Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class symbol_list(models.Model):
    _name = 'cryto_tracking.symbol_list'
    _description = 'รายการ Symbol'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    symbol_group_id = fields.Many2one('cryto_tracking.symbol_group', string="Symbol Group", tracking=True)
    name = fields.Char(size=150, string="Symbol Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    symbol_logo = fields.Image(string="Logo", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)


class cryto_tracking(models.Model):
    _name = 'cryto_tracking.cryto_tracking'
    _description = 'ข้อมูลรายการ Tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    exchange_id = fields.Many2one('cryto_tracking.exchange_list', string="Exchange Name", required=True, tracking=True)
    symbol_id = fields.Many2one('cryto_tracking.symbol_list', string="Symbol Name", required=True, tracking=True)
    tracking_date = fields.Datetime(string="Tracking At", default=lambda self: fields.Date.today(), tracking=True)
    lastPrice = fields.Float(string="last price", required=True, tracking=True)# "last": 913303,
    lowestAsk = fields.Float(string="lowestAsk", default="0.0", tracking=True)# "lowestAsk": 913839.79,
    highestBid = fields.Float(string="highestBid", default="0.0", tracking=True)# "highestBid": 913303.01,
    percentChange = fields.Float(string="percentChange", default="0.0", tracking=True)# "percentChange": 0.3,
    baseVolume = fields.Float(string="baseVolume", default="0.0", tracking=True)# "baseVolume": 50.62163798,
    quoteVolume = fields.Float(string="quoteVolume", default="0.0", tracking=True)# "quoteVolume": 46120153.06,
    isFrozen = fields.Float(string="isFrozen", default="0.0", tracking=True)# "isFrozen": 0,
    high24hr = fields.Float(string="high24hr", default="0.0", tracking=True)# "high24hr": 920606.38,
    low24hr = fields.Float(string="low24hr", default="0.0", tracking=True)# "low24hr": 900200,
    change = fields.Float(string="change", default="0.0", tracking=True)# "change": 2697.99,
    prevClose = fields.Float(string="prevClose", default="0.0", tracking=True)# "prevClose": 913303,
    prevOpen = fields.Float(string="prevOpen", default="0.0", tracking=True)# "prevOpen": 910605.01
    name = fields.Char(string="Symbol", compute="_value_symbol", store=True, tracking=True)
    exchange_name = fields.Char(string="Exchange", compute="_value_symbol", store=True, tracking=True)

    @api.depends('symbol_id', 'exchange_id')
    def _value_symbol(self):
        for record in self:
            record.name = record.symbol_id.name
            record.exchange_name = record.exchange_id.name