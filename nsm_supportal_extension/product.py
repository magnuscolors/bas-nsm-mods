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
import openerp.addons.decimal_precision as dp


class product_category(osv.osv):
    _inherit = "product.category"

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name'], context=context)
        res = []
        for record in reads:
            name = record['name']
            res.append((record['id'], name))
        return res

    def name_get_full(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get_full(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'supportal': fields.boolean('Parent Portal Productcategorieen',  help="Indicator that determines the role of this category as parent of supplier portal categories."),
    }

product_category()



#class product_product(osv.osv):
#    _inherit = 'product.product'
#
#    _columns = {
#        'avail_supplier_portal': fields.selection([('marketing', 'Marketing'),
#                                                   ('editorial', 'Editorial')],
#                                                  "Available Supplier Portal",),
#
#    }
#
#product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
