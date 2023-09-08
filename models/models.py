# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class crypto_tracking(models.Model):
#     _name = 'crypto_tracking.crypto_tracking'
#     _description = 'crypto_tracking.crypto_tracking'

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
    _name = 'crypto_tracking.exchange_list'
    _description = 'ข้อมูล Exchange'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    name = fields.Char(size=150, string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    api_url = fields.Text(string="API URL", required=True, tracking=True)
    api_key = fields.Text(string="API Key", required=True, tracking=True)
    api_secret = fields.Text(string="API Secret", required=True, tracking=True)
    api_passphrase = fields.Text(string="API Passphrase", tracking=True)
    exchange_logo = fields.Image(string="Logo", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class block_chain_network(models.Model):
    _name = 'crypto_tracking.block_chain_network'
    _description = 'ข้อมูล Network'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    name = fields.Char(size=150, string="Group Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    fee = fields.Float(string="Fee", default="0.00", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class symbol_group(models.Model):
    _name = 'crypto_tracking.symbol_group'
    _description = 'ข้อมูลประเภทของเหรียญ'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    name = fields.Char(size=150, string="Group Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class symbol_list(models.Model):
    _name = 'crypto_tracking.symbol_list'
    _description = 'ข้อมูลรายชื่อเหรียญ'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    symbol_group_id = fields.Many2one('crypto_tracking.symbol_group', string="Symbol Group", tracking=True)
    name = fields.Char(size=150, string="Symbol Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    symbol_logo = fields.Image(string="Logo", tracking=True)
    is_withdraw_only = fields.Boolean(string="Withdraw Only", default=False, tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class currency_pair(models.Model):
    _name = 'crypto_tracking.currency_pair'
    _description = 'ข้อมูลสกุลเงิน'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    name = fields.Char(size=150, string="Currency Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    currency_logo = fields.Image(string="Logo", tracking=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id, tracking=True)
    price = fields.Monetary(string="อัตราแลกเปลี่ยน/USD", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

class transfer_fee(models.Model):
    _name = 'crypto_tracking.transfer_fee'
    _description = 'ข้อมูลอัตราค่าธรรมเนียมการโอน'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    symbol_id = fields.Many2one('crypto_tracking.symbol_list', string="Symbol Name", required=True, tracking=True)
    block_chain_id = fields.Many2one('crypto_tracking.block_chain_network', string="Block Chain Network", required=True, tracking=True)
    name = fields.Char(string="Symbol Name", compute="_value_symbol", store=True, tracking=True)
    block_chain = fields.Char(string="Block Chain Network", compute="_value_symbol", store=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    fee = fields.Float(string="Fee", default="0.0", tracking=True)
    is_active = fields.Boolean(string="Is Active", default=False, tracking=True)

    @api.depends('symbol_id', 'block_chain_id')
    def _value_symbol(self):
        for record in self:
            record.name = record.symbol_id.name
            record.block_chain = record.block_chain_id.name

class crypto_tracking(models.Model):
    _name = 'crypto_tracking.crypto_tracking'
    _description = 'ข้อมูลการติดตามราคาในท้องตลาด'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']

    exchange_id = fields.Many2one('crypto_tracking.exchange_list', string="Exchange Name", required=True, tracking=True)
    symbol_id = fields.Many2one('crypto_tracking.symbol_list', string="Symbol Name", required=True, tracking=True)
    currency_pair_id = fields.Many2one('crypto_tracking.currency_pair', string="Currency Pair Name", required=True, tracking=True)
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
    currency_pair_name = fields.Char(string="Pair", compute="_value_symbol", store=True, tracking=True)
    exchange_name = fields.Char(string="Exchange", compute="_value_symbol", store=True, tracking=True)

    @api.depends('symbol_id', 'exchange_id','currency_pair_id')
    def _value_symbol(self):
        for record in self:
            record.name = record.symbol_id.name
            record.exchange_name = record.exchange_id.name
            record.currency_pair_name = record.currency_pair_id.name