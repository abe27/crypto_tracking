# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
import requests


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
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag already exists!"),
    ]
    name = fields.Char(size=150, string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    api_url = fields.Text(string="API URL", required=True, tracking=True)
    api_key = fields.Text(string="API Key", required=True, tracking=True)
    api_secret = fields.Text(string="API Secret", required=True, tracking=True)
    api_passphrase = fields.Text(string="API Passphrase", tracking=True)
    exchange_logo = fields.Image(string="Logo", tracking=True)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.user.company_id.currency_id, tracking=True)
    exchange_transfer_fee = fields.Monetary(
        string="Exchange Transfer", default=0.0, tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)


class block_chain_network(models.Model):
    _name = 'crypto_tracking.block_chain_network'
    _description = 'ข้อมูล Network'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag already exists!"),
    ]

    name = fields.Char(size=150, string="Group Name",
                       required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    fee = fields.Float(string="Fee", digits=(
        12, 8), default="0.00", tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)


class symbol_group(models.Model):
    _name = 'crypto_tracking.symbol_group'
    _description = 'ข้อมูลประเภทของเหรียญ'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag already exists!"),
    ]

    name = fields.Char(size=150, string="Group Name",
                       required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)


class symbol_list(models.Model):
    _name = 'crypto_tracking.symbol_list'
    _description = 'ข้อมูลรายชื่อเหรียญ'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag already exists!"),
    ]

    symbol_group_id = fields.Many2one(
        'crypto_tracking.symbol_group', string="Symbol Group", tracking=True)
    name = fields.Char(size=150, string="Symbol Name",
                       required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    symbol_logo = fields.Image(string="Logo", tracking=True)
    is_withdraw_only = fields.Boolean(
        string="Withdraw Only", default=False, tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)


class currency_pair(models.Model):
    _name = 'crypto_tracking.currency_pair'
    _description = 'ข้อมูลสกุลเงิน'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag already exists!"),
    ]

    name = fields.Char(size=150, string="Currency Name",
                       required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    currency_logo = fields.Image(string="Logo", tracking=True)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.user.company_id.currency_id, tracking=True)
    price = fields.Monetary(string="อัตราแลกเปลี่ยน/USD", tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)


class transfer_fee(models.Model):
    _name = 'crypto_tracking.transfer_fee'
    _description = 'ข้อมูลอัตราค่าธรรมเนียมการโอน'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    symbol_id = fields.Many2one(
        'crypto_tracking.symbol_list', string="Symbol Name", required=True, tracking=True)
    block_chain_id = fields.Many2one(
        'crypto_tracking.block_chain_network', string="Block Chain Network", required=True, tracking=True)
    name = fields.Char(string="Symbol Description",
                       compute="_value_symbol", store=True, tracking=True)
    # block_chain = fields.Char(string="Block Chain Network", compute="_value_symbol", store=True, tracking=True)
    description = fields.Text(string="Description", default="-", tracking=True)
    fee = fields.Float(string="Fee", digits=(
        12, 8), default="0.0", tracking=True)
    block_summary = fields.Float(string="จํานวน Block ที่ต้องรอ", digits=(
        12, 2), default="0.0", tracking=True)
    is_active = fields.Boolean(
        string="Is Active", default=False, tracking=True)

    @api.depends('symbol_id', 'block_chain_id')
    def _value_symbol(self):
        for record in self:
            record.name = record.symbol_id.description
            # record.block_chain = record.block_chain_id.name


class crypto_tracking(models.Model):
    _name = 'crypto_tracking.crypto_tracking'
    _description = 'ข้อมูลการติดตามราคาในท้องตลาด'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    exchange_id = fields.Many2one(
        'crypto_tracking.exchange_list', string="Exchange Name", required=True, tracking=True)
    symbol_id = fields.Many2one(
        'crypto_tracking.symbol_list', string="Symbol Name", required=True, tracking=True)
    currency_pair_id = fields.Many2one(
        'crypto_tracking.currency_pair', string="Currency Pair Name", required=True, tracking=True)
    name = fields.Char(string="Symbol", required=True, tracking=True)
    tracking_date = fields.Datetime(
        string="Tracking At", default=lambda self: fields.Datetime.now(), tracking=True)
    lastPrice = fields.Float(string="last price", digits=(
        12, 8), required=True, tracking=True)  # "last": 913303,
    lowestAsk = fields.Float(string="lowestAsk", digits=(
        12, 8), default="0.0", tracking=True)  # "lowestAsk": 913839.79,
    highestBid = fields.Float(string="highestBid", digits=(
        12, 8), default="0.0", tracking=True)  # "highestBid": 913303.01,
    percentChange = fields.Float(string="percentChange", digits=(
        12, 2), default="0.0", tracking=True)  # "percentChange": 0.3,
    baseVolume = fields.Float(string="baseVolume", digits=(
        12, 8), default="0.0", tracking=True)  # "baseVolume": 50.62163798,
    quoteVolume = fields.Float(string="quoteVolume", digits=(
        12, 8), default="0.0", tracking=True)  # "quoteVolume": 46120153.06,
    isFrozen = fields.Float(string="isFrozen", digits=(
        12, 8), default="0.0", tracking=True)  # "isFrozen": 0,
    high24hr = fields.Float(string="high24hr", digits=(
        12, 8), default="0.0", tracking=True)  # "high24hr": 920606.38,
    low24hr = fields.Float(string="low24hr", digits=(
        12, 8), default="0.0", tracking=True)  # "low24hr": 900200,
    change = fields.Float(string="change", digits=(
        12, 8), default="0.0", tracking=True)  # "change": 2697.99,
    prevClose = fields.Float(string="prevClose", digits=(
        12, 8), default="0.0", tracking=True)  # "prevClose": 913303,
    prevOpen = fields.Float(string="prevOpen", digits=(
        12, 8), default="0.0", tracking=True)  # "prevOpen": 910605.01
    is_status = fields.Selection([
        ("0", "Start"),
        ("1", "Wait"),
        ("2", "Done"),
    ], string="Status", default="0", tracking=True)
    symbol_image = fields.Image(compute="_value_symbol", store=True)
    exchange_image = fields.Image(compute="_value_symbol", store=True)
    pair_image = fields.Image(compute="_value_symbol", store=True)

    line_ids = fields.One2many("crypto_tracking.history", "crypto_tracking_id", string="History", tracking=True)

    def write(self, obj):
        obj["tracking_date"] = fields.Datetime.now()
        res = super().write(obj)
        return res

    @api.model_create_multi
    def create(self, obj):
        result = super().create(obj)
        return result

    @api.depends('symbol_id', 'exchange_id', 'currency_pair_id')
    def _value_symbol(self):
        for record in self:
            record.symbol_image = record.symbol_id.symbol_logo
            record.exchange_image = record.exchange_id.exchange_logo
            record.pair_image = record.currency_pair_id.currency_logo

    def reloadData(self):
        if self.is_status == "1":
            symbol = str(f"{self.currency_pair_id.name}_{self.symbol_id.name}").strip()
            #### Get Data
            response = requests.request( "GET", f"https://api.bitkub.com/api/market/ticker?sym={symbol}")
            obj = response.json()
            self.is_status = "1"
            data = obj[symbol]
            self.tracking_date = fields.Datetime.now()
            self.lastPrice = data["last"]
            self.lowestAsk = data["lowestAsk"]
            self.highestBid = data["highestBid"]
            self.percentChange = data["percentChange"]
            self.baseVolume = data["baseVolume"]
            self.quoteVolume = data["quoteVolume"]
            self.isFrozen = data["isFrozen"]
            self.high24hr = data["high24hr"]
            self.low24hr = data["low24hr"]
            self.change = data["change"]
            self.prevClose = data["prevClose"]
            self.prevOpen = data["prevOpen"]
            self.is_status = "2"

            ### Create History
            self.env['crypto_tracking.history'].create({
                'crypto_tracking_id': self._origin.id,
                "sync_at": fields.Datetime.now(),
                "name": self.symbol_id.name,
                "pair": "THB",
                "price": data["last"],
                "percentChange": data["percentChange"],
                "baseVolume": data["baseVolume"],
                "quoteVolume": data["quoteVolume"],
            })
        else:
            if self.is_status == "2":
                self.is_status = "0"
                
            elif self.is_status == "0":
                self.is_status = "1"
            


class history(models.Model):
    _name = 'crypto_tracking.history'
    _description = 'ข้อมูลประวัติราคา'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']

    crypto_tracking_id = fields.Many2one('crypto_tracking.crypto_tracking', required=True, tracking=True)
    sync_at = fields.Datetime(
        string="Sync At", default=lambda self: fields.Datetime.now(), tracking=True)
    name = fields.Char(string="Symbol", required=True, tracking=True)
    pair = fields.Char(string="Pair", required=True, tracking=True)
    price = fields.Float(string="Price", digits=(12, 8),required=True, tracking=True)
    percentChange = fields.Float(string="percentChange", digits=(12, 2), default="0.0", tracking=True)
    baseVolume = fields.Float(string="baseVolume", digits=(12, 8), default="0.0", tracking=True)
    quoteVolume = fields.Float(string="quoteVolume", digits=(12, 8), default="0.0", tracking=True)
    exchange_id = fields.Many2one('crypto_tracking.exchange_list', compute="_value_exchange", store=True, tracking=True)

    def write(self, obj):
        obj["sync_at"] = fields.Datetime.now()
        res = super().write(obj)
        return res

    @api.model_create_multi
    def create(self, obj):
        obj[0]["sync_at"] = fields.Datetime.now()
        result = super().create(obj)
        return result

    @api.depends('crypto_tracking_id')
    def _value_exchange(self):
        for record in self:
            record.exchange_id = record.crypto_tracking_id.exchange_id