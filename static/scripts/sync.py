import xmlrpc.client
import pandas as pd
import sys


odoo_url = "http://localhost:8081"
odoo_db = "odoo"
odoo_username = 'admin'
odoo_password = "admin"

def main():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
    print(common.version())


    uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))
    if uid:
        print(uid)
        ### Sync Exchange


        ### Sync Symbol Group


        ### Sync Symbol

if __name__ == '__main__':
    main()
    sys.exit(0)