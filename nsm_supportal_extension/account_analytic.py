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

class account_analytic(osv.osv):
    _inherit = 'account.analytic.account'


    def _supplier_analytic_search(self, cr, uid, obj, name, args,  context=None):
        res_user_obj = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        supplier_id = res_user_obj.partner_id.id or False
        if not supplier_id:
            return
        supplier_obj = self.pool.get('res.partner').browse(cr, uid, supplier_id, context=context)
        accids = [acc.id for acc in supplier_obj.analytic_account_ids]
        if accids :
            anacc_ids = self.search(cr, uid, [('id', 'in', accids)],)
            return [('id','in', anacc_ids)]

        anacc2_ids = self.search(cr, uid, [(1,'=',1)], context=context)
        return [('id','in', anacc2_ids)]



    _columns = {
        'supp_analytic_accids': fields.function(lambda self, cr, uid, ids, field_name, arg, context=None: dict.fromkeys(ids, True), fnct_search=_supplier_analytic_search, type='boolean', method=True,),
    }


account_analytic()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
