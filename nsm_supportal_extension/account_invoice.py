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

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


class custom_account_invoice(osv.osv):
    _inherit = 'account.invoice'

   

    _columns = {
        'product_category': fields.many2one('product.category', 'Cost Category'),
    }

    def act_submit(self, cr, uid, ids, context={}):
        sale_team_obj = False
        sale_team_pool = self.pool.get('sales.team')
        for self_obj in self.browse(cr, uid, ids, context=context):
            if not self_obj.file:
                raise osv.except_osv(_('Error!'), _('Please Upload your invoice File before submit.'))
            if self_obj.reuse and not self_obj.terms:
                raise osv.except_osv(_('Error!'), _('Please Accept re-use terms'))
            if not self_obj.invoice_line:
                raise osv.except_osv(_('No Invoice Lines!'), _('Please create some invoice lines.'))
            sale_team_id = sale_team_pool.search(
                cr, uid, [('analytic_account_id', '=', self_obj.main_account_analytic_id.id),
                          ('product_cat_id', '=', (self_obj.invoice_line and
                                                   self_obj.invoice_line[0].product_id.categ_id and
                                                   self_obj.invoice_line[0].product_id.categ_id.id or False)) or False
                         ],
                context=context)
        if sale_team_id:
                sale_team_obj = sale_team_pool.browse(cr, uid, sale_team_id[0], context=context)

        date = time.strftime('%Y-%m-%d')
        self.write(cr, uid, ids, {'is_submitted': True, 'date_invoice': date,
                                   'section_id': sale_team_obj and sale_team_obj.sales_team_id.id or False,
                                   'user_id':  sale_team_obj and sale_team_obj.sales_team_id.user_id.id or False})
        self.button_reset_taxes(cr, uid, ids, context=context)
        return True

    def onchange_main_analytic_ac(self, cr, uid, ids, main_analytic, context={}):
        if not main_analytic:
            return {'value': {'sub_account_analytic_id': False}}
        return {}


    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """

        res = {}
        res = super(custom_account_invoice, self).fields_view_get(cr, user, view_id, view_type,
                                                       context, toolbar=toolbar, submenu=submenu)
        if not context.get('is_portal'):
            return res
        res['toolbar'] = {'print': [], 'other': []}
        return res

custom_account_invoice()


class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
        'new_tax_id': fields.many2one('account.tax', 'Tax',),
    }

    def onchange_tax_id(self, cr, uid, ids, tax_id, context={}):
        if not tax_id:
            return {'value': {'invoice_line_tax_id': []}}
        return {'value': {'invoice_line_tax_id': [tax_id]}}

    def product_id_change(self, cr, uid, ids, product, uom_id,
                          qty=0, name='', type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False, currency_id=False,
                          context=None, company_id=None):
        res = super(account_invoice_line, self).product_id_change(
            cr, uid, ids, product=product, uom_id=uom_id, qty=qty, name=name,
            type=type, partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            context=context, company_id=company_id)
        if context is None:
            context = {}
        if not context.get('is_portal'):
            return res
        uom_pool = self.pool.get('product.uom')
        account_tax_pool = self.pool.get('account.tax')
        uom_search_id = uom_pool.search(
            cr, uid, [('name', '=', 'Piece')], context=context)
        res['value'].update({'new_tax_id': res['value']['invoice_line_tax_id'][:1] or False})
        if not uom_search_id:
            return res
        res['value'].update({'uos_id': uom_search_id[0], })
        return res

account_invoice_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
