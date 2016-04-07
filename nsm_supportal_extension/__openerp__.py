# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Magnus
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
    'name': 'NSM Leveranciers Portaal uitbreiding',
    'version': '1.0',
    'category': 'Invoice',
    'summary': 'NSM Leveranciers Portaal Uitbreiding',
    'description': """
    New Skool Media Leveranciers Portaal uitbreiding.
    """,
    'author': 'Magnus',
    'website': 'http://www.magnus.nl',
    'depends': ['nsm_supplier_portal','nsm_improv02' ],
    'data': [
        "account_invoice_workflow.xml",
        "account_invoice_view.xml",
        "res_partner_view.xml",
        "product_view.xml",
        "analytic_line.xml",
        "supportal_extension_security_view.xml",
    ],
    'demo': [],
    'test': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
