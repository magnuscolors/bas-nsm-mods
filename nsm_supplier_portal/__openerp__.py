# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014 BAS Solutions
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Supplier Portal',
    'version': '1.0',
    'category': 'Invoice',
    'summary': 'Invoice',
    'description': """This module holds the BAS-ERP Portal enhanchements.
    """,
    'author': 'BAS Solutions',
    'website': 'http://www.bas-solutions.nl',
    'depends': ['base', 'account', 'mail', 'account_analytic_analysis', 'portal', 'sale_crm', 'megis_auth', 'megis_improv', 'web_m2x_options'],
    'data': [
        "data/crm_sale_team_data.xml",
        "security/supplier_portal_security_view.xml",
        "security/ir.model.access.csv",
        "mail_thread_view.xml",
        "res_partner_view.xml",
        "account_invoice_view.xml",
        "supplier_invoice_view.xml",
        "product_view.xml",
        "account_analytic_view.xml",
        "menu_view.xml",
        "res_config_view.xml",
        "res_company_view.xml",
        "sales_team_view.xml",
        "wizard/generate_mapping_view.xml",
        "res_bank_view.xml",
    ],
    'demo': [],
    'test': [
    ],
    'qweb': [
        'static/src/xml/mail.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
