# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields


class custom_account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'supplier_id': fields.many2one('res.partner', 'Supplier',),
        'main_account_analytic_id': fields.many2one('account.analytic.account', 'Main Analytic account'),
        'sub_account_analytic_id': fields.many2one('account.analytic.account', 'Sub Analytic account'),
    }

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
