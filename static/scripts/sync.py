import xmlrpc.client
import pandas as pd
import sys
import requests
from datetime import datetime


odoo_url = "http://localhost:8081"
odoo_db = "odoo"
odoo_username = 'sync'
odoo_password = "sync"
# f96bd49d955794f770df528454b505bc1667669b


def main():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
    # print(common.version())

    uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))
    if uid:
        try:
            # Get Bitkub Ticker
            exchange = models.execute_kw(odoo_db, uid, odoo_password, 'crypto_tracking.exchange_list', 'search', [
                [['name', '=', "Bitkub"]]])
            currency = models.execute_kw(odoo_db, uid, odoo_password, 'crypto_tracking.currency_pair', 'search', [
                [['name', '=', "THB"]]])
            response = requests.request(
                "GET", "https://api.bitkub.com/api/market/ticker")
            obj = response.json()
            for key in obj:
                data = obj[key]
                sym = str(key.replace('THB_', '')).strip()
                symbol = models.execute_kw(
                    odoo_db, uid, odoo_password, 'crypto_tracking.symbol_list', 'search', [[['name', '=', sym]]])

                isDuplicate = models.execute_kw(odoo_db, uid, odoo_password, 'crypto_tracking.crypto_tracking', 'search', [
                                                [['exchange_id', '=', exchange[0]], ['symbol_id', '=', symbol[0]]]])
                insData = {
                    "name": key,
                    "exchange_id": exchange[0],
                    "symbol_id": symbol[0],
                    "currency_pair_id": currency[0],
                    "lastPrice": data["last"],
                    "lowestAsk": data["lowestAsk"],
                    "highestBid": data["highestBid"],
                    "percentChange": data["percentChange"],
                    "baseVolume": data["baseVolume"],
                    "quoteVolume": data["quoteVolume"],
                    "isFrozen": data["isFrozen"],
                    "high24hr": data["high24hr"],
                    "low24hr": data["low24hr"],
                    "change": data["change"],
                    "prevClose": data["prevClose"],
                    "prevOpen": data["prevOpen"],
                }

                historyData = {
                    "name": sym,
                    "pair": "THB",
                    "price": data["last"],
                    "percentChange": data["percentChange"],
                    "baseVolume": data["baseVolume"],
                    "quoteVolume": data["quoteVolume"],
                }

                if len(isDuplicate) > 0:
                    ids = models.execute_kw(odoo_db, uid, odoo_password, 'crypto_tracking.crypto_tracking','write', [isDuplicate,insData])
                    print(f"{isDuplicate} ==> UPDATE {key}::{ids}")
                    historyData['crypto_tracking_id'] = isDuplicate[0]
                else:
                    ids = models.execute_kw(
                        odoo_db, uid, odoo_password, 'crypto_tracking.crypto_tracking', 'create', [insData])

                    print(f"{ids} ==> INSERT {key}")
                    historyData['crypto_tracking_id'] = ids

                ### Create History
                models.execute_kw(
                        odoo_db, uid, odoo_password, 'crypto_tracking.history', 'create', [historyData])

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
    sys.exit(0)
