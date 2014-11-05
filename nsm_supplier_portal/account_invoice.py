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


class custom_account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'supplier_id': fields.many2one('res.partner', 'Supplier',),
        'main_account_analytic_id': fields.many2one('account.analytic.account', 'Main Analytic account'),
        'sub_account_analytic_id': fields.many2one('account.analytic.account', 'Sub Analytic account'),
    }

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def create(self, cr, uid, vals, context={}):
        follower_ids = []
        partner_id = self.pool.get('res.partner').browse(
            cr, uid, vals['partner_id'], context=context)
        if partner_id.message_follower_ids:
            for follower_id in partner_id.message_follower_ids:
                follower_ids.append(follower_id.id)
        vals['message_follower_ids'] = follower_ids
        res = super(account_invoice, self).create(
            cr, uid, vals, context=context)
        obj = self.browse(cr, uid, res, context=context)
        partner_ids = []
        if obj.partner_id.message_follower_ids:
            for follower_id in partner_id.message_follower_ids:
                partner_ids.append(follower_id.id)
        partner_id = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).partner_id.id
        if partner_id in partner_ids:
            partner_ids.remove(partner_id)
        if obj.message_ids:
            for msg in obj.message_ids:
             self.pool.get('mail.notification')._notify(
                 cr, uid, msg.id, partners_to_notify=partner_ids,
                 context=context)
        return res

    def _get_supplier(self, cr, uid, ids, context={}):
        res_user_obj = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return res_user_obj.partner_id.id or False
        
    def supplier_id_change(self, cr, uid, ids, supplier_id, context={}):
        res = {}
        if not supplier_id:
            return res
        res = {'value': {'partner_id': supplier_id}}
        return res 
    _defaults = {
        'supplier_id': _get_supplier,
    }

custom_account_invoice()

#product_packaging
class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    
    _columns = {
        'file': fields.many2one('ir.attachment', "Upload File")
    }
    def onchange_product_id(self, cr, uid, ids, product_id, context={}):
        res = {}
        if not product_id:
            return res
        product_obj = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        res = {'value': {'name': product_obj.name}}
        return res
account_invoice_line()
 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
