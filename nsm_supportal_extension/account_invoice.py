# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2016 Magnus www.magnus.nl
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

import openerp.addons.decimal_precision as dp

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time

from openerp import api, fields as fields1, models, _

class custom_account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_state(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('state', 'draft')

    def _get_reference_type(self, cr, uid, context=None):
        return [('none', _('Free Reference'))]


    _columns = {

        'product_category': fields.many2one('product.category', 'Cost Category',domain=[('parent_id.supportal', '=', True)]),
        # 'main_account_analytic_id': fields.many2one('account.analytic.account', 'Main Analytic account', domain=[('type','=','view'), ('portal_main', '=', True)]),
        'main_account_analytic_id': fields.many2one('account.analytic.account', 'Main Analytic account', domain=[('portal_main', '=', True)]),
        'state': fields.selection([
            ('portalcreate','Niet Ingediend'),
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('auth','Goedgekeurd'),
            ('verified','Verified'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ],'Status', select=True, readonly=True, track_visibility='onchange',
            help='* The \'Niet Ingediend\' status is used when a Portal user is encoding a new and unconfirmed Invoice, before it gets submitted. \
            \n* The \'Draft\' status is used when an accounting user is encoding a new and unconfirmed Invoice or when a Portal user submitted it. \
            \n* The \'Pro-forma\' when invoice is in Pro-forma status,invoice does not have an invoice number. \
            \n* The \'Open\' status is used when user confirms invoice, a invoice number is generated. It is in open status till user authorizes invoice. \
            \n* The \'Goedgekeurd\' status is used when invoice is authorized for payment. \
            \n* The \'Verified\' status is used when invoice is already authorized, but not yet confirmed for payment, because it is of higher value than Company Verification treshold. \
            \n* The \'Paid\' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled. \
            \n* The \'Cancelled\' status is used when user cancel invoice.'),
        'name': fields.char('Description', size=64, select=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'origin': fields.char('Source Document', size=64, help="Reference of the document that produced this invoice.", readonly=True, states={'draft':[('readonly',False)]}),
        'supplier_invoice_number': fields.char('Supplier Invoice Number', size=64, help="The reference of this invoice as provided by the supplier.", readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'reference_type': fields.selection(_get_reference_type, 'Payment Reference',
            required=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'date_invoice': fields.date('Invoice Date', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, select=True, help="Keep empty to use the current date"),
        'date_due': fields.date('Due Date', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, select=True,
            help="If you use payment terms, the due date will be computed automatically at the generation "\
                "of accounting entries. The payment term may compute several due dates, for example 50% now and 50% in one month, but if you want to force a due date, make sure that the payment term is not set on the invoice. If you keep the payment term and the due date empty, it means direct payment."),
        'partner_id': fields.many2one('res.partner', 'Partner', change_default=True, readonly=True, required=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, track_visibility='always'),
        'payment_term': fields.many2one('account.payment.term', 'Payment Terms',readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]},
            help="If you use payment terms, the due date will be computed automatically at the generation "\
                "of accounting entries. If you keep the payment term and the due date empty, it means direct payment. "\
                "The payment term may compute several due dates, for example 50% now, 50% in one month."),
        # 'period_id': fields.many2one('account.period', 'Force Period', domain=[('state','<>','done')], help="Keep empty to use the period of the validation(invoice) date.", readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'account_id': fields.many2one('account.account', 'Account', required=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, help="The partner account used for this invoice."),
        # 'invoice_line': fields.one2many('account.invoice.line', 'invoice_id', 'Invoice Lines', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        # 'tax_line': fields.one2many('account.invoice.tax', 'invoice_id', 'Tax Lines', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),

        'currency_id': fields.many2one('res.currency', 'Currency', required=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, track_visibility='always'),
        'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]},
                                      domain="[('type', 'in', {'out_invoice': ['sale'], 'out_refund': ['sale_refund'], 'in_refund': ['purchase_refund'], 'in_invoice': ['purchase']}.get(type, [])), ('company_id', '=', company_id)]"),
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'check_total': fields.float('Verification Total', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'partner_bank_id': fields.many2one('res.partner.bank', 'Bank Account',
            help='Bank Account Number to which the invoice will be paid. A Company bank account if this is a Customer Invoice or Supplier Refund, otherwise a Partner bank account number.', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        # 'move_name': fields.char('Journal Entry', size=64, readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),

        'user_id': fields.many2one('res.users', 'Salesperson', readonly=True, track_visibility='onchange', states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)],'open':[('readonly',False)]}),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position', readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}),
        'topf': fields.boolean('To Portal Flow', states={'draft':[('readonly',False)]}, help="Checking makes routing to Portal Flow possible"),
        #'create_uid': fields.many2one('res.user', readonly=True ),
    }

    _defaults = {
        'state': _get_state,
        'company_id': lambda self,cr,uid,c:
            self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
    }

    def supplier_id_change(self, cr, uid, ids, supplier_id, company_id, context={}):
        res = {}
        if not supplier_id:
            return res
        supplier = self.pool.get('res.partner').browse(cr, uid, supplier_id, context=context)

        res =   {'value': {
                'partner_id': supplier_id,
                'reuse': supplier.reuse,
                'is_portal': True,
                }}

        return res


    def product_category_change(self, cr, uid, ids, product_category, context={}):
        res = {}
        if not ids:
            return res
        inv_obj = self.browse(cr,uid,ids)
        llist = []
        if inv_obj[0].invoice_line_ids:
            for line in inv_obj[0].invoice_line_ids:
                if line.product_id:
                    llist.append((1, line.id, {'product_id': [],}))
            res = { 'value': { 'invoice_line_ids': llist },'warning': {'title': 'Let op!', 'message': 'U heeft de Factuurcategorie aangepast. Nu moet u opnieuw product(-en) en Edities/Kostenplaatsen selecteren in de factuurregel(s)'}}
        return res

    def onchange_main_analytic_ac(self, cr, uid, ids, main_analytic, context={}):
        res = {}
        if not ids:
            return res
        inv_obj = self.browse(cr,uid,ids)
        llist = []
        if inv_obj[0].invoice_line_ids:
            for line in inv_obj[0].invoice_line_ids:
                if line.account_analytic_id:
                    llist.append((1, line.id, {'account_analytic_id': [],}))
            res = { 'value': { 'invoice_line_ids': llist },'warning': {'title': 'Let op!', 'message': 'U heeft de Titel/Afdeling aangepast. Nu moet u opnieuw Edities/Kostenplaatsen selecteren in de factuurregel(s)'}}
        return res



    def act_submit(self, cr, uid, ids, context={}):
        sale_team_obj = False
        sale_team_pool = self.pool.get('sales.team')
        for self_obj in self.browse(cr, uid, ids, context=context):
            if not self_obj.file:
                raise osv.except_osv(_('Error!'), _('Please Upload your invoice File before submit.'))
            if self_obj.reuse and not self_obj.terms:
                raise osv.except_osv(_('Error!'), _('Please Accept re-use terms'))
            if not self_obj.invoice_line_ids:
                raise osv.except_osv(_('No Invoice Lines!'), _('Please create some invoice lines.'))
            sale_team_id = sale_team_pool.search(
                cr, uid, [('analytic_account_id', '=', self_obj.main_account_analytic_id.id),
                          ('product_cat_id', '=', (self_obj.invoice_line_ids and
                                                   self_obj.invoice_line_ids[0].product_id.categ_id and
                                                   self_obj.invoice_line_ids[0].product_id.categ_id.id or False)) or False
                         ],
                context=context)
            if sale_team_id:
                sale_team_obj = sale_team_pool.browse(cr, uid, sale_team_id[0], context=context)

            date = time.strftime('%Y-%m-%d')
            self.write(cr, uid, ids, {'is_portal': True,
                                    'date_invoice': date,
                                    'state': 'draft',
                                    'section_id': sale_team_obj and sale_team_obj.sales_team_id.id or False,
                                    'user_id':  sale_team_obj and sale_team_obj.sales_team_id.user_id.id or False})
            # self.button_reset_taxes(cr, uid, ids, context=context)
        return True

    def act_portal_back(self, cr, uid, ids, context={}):
        for self_obj in self.browse(cr, uid, ids, context=context):
            cr.execute('SELECT create_uid FROM account_invoice WHERE id=%s', (self_obj.id,))
            res_user_id = cr.fetchone()
            [res_user_obj] = self.pool.get('res.users').browse(cr, uid, [res_user_id[0]], context=context)
            if not self_obj.supplier_id or self_obj.supplier_id is not self_obj.partner_id:
                if not res_user_obj.partner_id or res_user_obj.partner_id.id is not self_obj.partner_id.id:
                    self.write(cr, uid, ids,({'state':'portalcreate','is_portal': False, 'topf': True, 'supplier_id': self_obj.partner_id and self_obj.partner_id.id or False}))
                else:
                    self.write(cr, uid, ids,({'state':'portalcreate','is_portal': False, 'supplier_id': self_obj.partner_id and self_obj.partner_id.id or False}))
            if not res_user_obj.partner_id or res_user_obj.partner_id.id is not self_obj.partner_id.id:
                self.write(cr, uid, ids,({'state':'portalcreate','is_portal': False, 'topf': True }))
            else:
                self.write(cr, uid, ids,({'state':'portalcreate','is_portal': False }))
        return True

custom_account_invoice()

class Invoice(models.Model):
    _inherit = ["account.invoice"]

    move_name = fields1.Char(string='Journal Entry', readonly=False,
        default=False, copy=False, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]},
        help="Technical field holding the number given to the invoice, automatically set when the invoice is validated then stored to set the same number again if the invoice is cancelled, set to draft and re-validated.")

    invoice_line_ids = fields1.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines', oldname='invoice_line',
        readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, copy=True)
    tax_line_ids = fields1.One2many('account.invoice.tax', 'invoice_id', string='Tax Lines', oldname='tax_line',
        readonly=True, states={'draft':[('readonly',False)],'portalcreate':[('readonly',False)]}, copy=True)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
