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

from openerp import models, fields as fields2, api, _


class custom_account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_file(self, cr, uid, ids, name, args, context={}):
        res = {}
        att_pool = self.pool.get('ir.attachment')
        for self_id in ids:
            att_ids = att_pool.search(cr, uid, [('res_id', '=', self_id),
                                                ('res_model', '=',
                                                 self._name)], order='id')
            data = False
            if att_ids:
                att_data = att_pool.read(cr, uid, att_ids, ['datas'])

                data = att_data[0]['datas']
            res[self_id] = data
        return res

    def _set_file(self, cr, uid, id, name, value, args, context={}):
        att_pool = self.pool.get('ir.attachment')
        att_ids = att_pool.search(cr, uid, [('res_id', '=', id),
                                            ('res_model', '=',
                                             self._name)], order='id')
        self_obj = self.browse(cr, uid, id, context=context)
        if not value:
            return True
        if att_ids:
            att_pool.write(cr, uid, att_ids[0],
                           {'datas': value,
                            'datas_fname':
                            self_obj.data_supplier_terms_file_name})
        else:
            att_pool.create(cr, uid,
                            {'datas': value,
                             'datas_fname':
                             self_obj.data_file,
                             'name': self_obj.data_file,
                             'res_id': self_obj.id, 'res_model': self._name,
                             'type': 'binary'
                            })
        return True

    def _get_supp_file(self, cr, uid, ids, name, args, context={}):
        res = {}
        company_pool = self.pool.get('res.company')
        company_id = company_pool._company_default_get(
            cr, uid, 'account.invoice', context=context)
        data = company_pool.browse(cr, uid, company_id,
                                   context=context).supplier_terms
        for self_id in ids:
            res[self_id] = data
        return res

    def _set_supp_file(self, cr, uid, id, name, value, args, context={}):
        return True

    _columns = {
        'supplier_id': fields.many2one('res.partner', 'Supplier',),
        'main_account_analytic_id': fields.many2one('account.analytic.account', 'Main Analytic account'),
        'sub_account_analytic_id': fields.many2one('account.analytic.account', 'Sub Analytic account'),
        'is_portal': fields.boolean('Portal'),
        'data_file': fields.char('File Name'),
        'supplier_terms': fields.function(
            _get_supp_file, fnct_inv=_set_supp_file, type='binary', string="Supplier Invoice Reuse-authorization File"),
        'is_submitted': fields.boolean('Submitted'),
        'supplier_ref_related': fields.related("supplier_invoice_number", type="char", size=256),
        'avail_supplier_portal': fields.selection([('marketing', 'Marketing'),
                                                   ('editorial', 'Editorial')],
                                                  "Available Supplier Portal",),
        'data_supplier_terms_file_name': fields.char('File Name'),
        'file': fields.function(
            _get_file, fnct_inv=_set_file, type='binary',
            string="Upload Your Invoice"),
        'terms': fields.boolean('I accept the re-use terms'),
        'reuse': fields.boolean('Reuse'),

    }

    def _get_terms(self, cr, uid, context=None):
        context = context or {}
        company_id = self.pool.get('res.company')._company_default_get(
            cr, uid, 'account.invoice', context=context)
        company_obj = self.pool.get('res.company').browse(
            cr, uid, company_id, context=context)
        if company_obj.supplier_terms:
            return company_obj.supplier_terms
        return False

    def _get_term_file_name(self, cr, uid, context=None):
        context = context or {}
        company_id = self.pool.get('res.company')._company_default_get(
            cr, uid, 'account.invoice', context=context)
        company_obj = self.pool.get('res.company').browse(
            cr, uid, company_id, context=context)
        if company_obj.supplier_terms and company_obj.data_fname:
            return company_obj.data_fname
        return False

    # --deep: rewritten this method below
    # def create(self, cr, uid, vals, context={}):
    #     follower_ids = []
    #     partner_id = self.pool.get('res.partner').browse(
    #         cr, uid, vals['partner_id'], context=context)
    #     if partner_id.message_follower_ids:
    #         for follower_id in partner_id.message_follower_ids:
    #             follower_ids.append(follower_id.id)
    #     vals['message_follower_ids'] = follower_ids
    #
    #     res = super(custom_account_invoice, self).create(
    #         cr, uid, vals, context=context)
    #     obj = self.browse(cr, uid, res, context=context)
    #     partner_ids = []
    #     if obj.partner_id.message_follower_ids:
    #         for follower_id in partner_id.message_follower_ids:
    #             partner_ids.append(follower_id.id)
    #     partner_id = self.pool.get('res.users').browse(
    #         cr, uid, uid, context=context).partner_id.id
    #     if partner_id in partner_ids:
    #         partner_ids.remove(partner_id)
    #     if obj.message_ids:
    #         for msg in obj.message_ids:
    #          self.pool.get('mail.notification')._notify(
    #              cr, uid, msg.id, partners_to_notify=partner_ids,
    #              context=context)
    #     return res

    def _get_supplier(self, cr, uid, ids, context={}):
        res_user_obj = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return res_user_obj.partner_id.id or False

    def supplier_id_change(self, cr, uid, ids, supplier_id, context={}):
        res = {}
        if not supplier_id:
            return res
        supplier = self.pool.get('res.partner').browse(cr, uid, supplier_id,
                                                       context=context)
        res = {'value': {'partner_id': supplier_id, 'reuse': supplier.reuse}}
        return res

    _defaults = {
        'supplier_id': _get_supplier,
        'supplier_terms': _get_terms,
        'data_supplier_terms_file_name': _get_term_file_name,
    }

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
        res = super(custom_account_invoice, self).fields_view_get(cr, user, view_id=view_id, view_type=view_type,
                                                       context=context, toolbar=toolbar, submenu=submenu)
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
        print "onchange_tax_id"
        if not tax_id:
            return {'value': {'invoice_line_tax_id': []}}
        return {'value': {'invoice_line_tax_id': [tax_id]}}

    # -- deep
    # def product_id_change(self, cr, uid, ids, product, uom_id,
    #                       qty=0, name='', type='out_invoice', partner_id=False,
    #                       fposition_id=False, price_unit=False, currency_id=False,
    #                       context=None, company_id=None):

    def product_id_change(self, cr, uid, ids, product, uom_id,
                          qty=0, name='', type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False, currency_id=False,
                          company_id=None, context=None):

        res = super(account_invoice_line, self).product_id_change(
            cr, uid, ids, product=product, uom_id=uom_id, qty=qty, name=name,
            type=type, partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            context=context, company_id=company_id)

        print "product_id_change deep", res

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


class Invoice(models.Model):
    _inherit = 'account.invoice'

    # --deep
    @api.multi
    def _add_followers_notify(self):
        """
            Adding followers of Partner to Invoice
        """
        self.ensure_one()
        mappedPartner = map(lambda x: x.partner_id.id, self.message_follower_ids)

        PartnerIDs = []
        for mf in self.partner_id.message_follower_ids:
            if mf.partner_id.id in mappedPartner: continue
            PartnerIDs.append(mf.partner_id.id)

        if not PartnerIDs:
            return False

        mail_invite = self.env['mail.wizard.invite'].with_context({
            'default_res_model': self._name,
            'default_res_id': self.id}).create({
            'partner_ids': [(4, PartnerIDs)], 'send_mail': True})
        return mail_invite.add_followers()


    @api.model
    def create(self, vals):
        res = super(Invoice, self).create(vals)
        res._add_followers_notify()
        return res


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(InvoiceLine, self)._onchange_product_id()
        print "_onchange_product_id", res
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
