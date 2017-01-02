# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2016 Magnus www.magnus.nl w.hulshof@magnus.nl
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


class sales_team(osv.osv):
    _inherit = 'sales.team'



    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True,),
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c:
            self.pool.get('res.company')._company_default_get(cr, uid, 'sales.team', context=c),

    }

class generate_mapping(osv.osv_memory):
    _inherit = 'generate.mapping'



    _defaults = {
        'state': 'draft',
    }

    def generate_mapping(self, cr, uid, ids, context={}):
        context = context or {}
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        company_id = context.get('company_id', user.company_id.id)
        analytic_ac_pool = self.pool.get('account.analytic.account')
        product_category_pool = self.pool.get('product.category')
        sales_team_pool = self.pool.get('sales.team')
        crm_sales_pool = self.pool.get('crm.case.section')
        existing_counter = 0
        created_counter = 0
        total = 0

        analytic_search_ids = analytic_ac_pool.search(
            cr, uid, [('portal_main', '=',  True),'|',('company_id','=', company_id),('company_id','=', False)], context=context)
        product_cat_ids = product_category_pool.search(
            cr, uid, [('parent_id.supportal', '=', True)], context=context)

        view_ref = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'nsm_supplier_portal', 'section_sales_department1')
        view_id = view_ref and view_ref[1] or False,

        for analytic_obj in analytic_ac_pool.browse(
            cr, uid, analytic_search_ids, context=context):
            for product_cat_obj in product_category_pool.browse(cr, uid, product_cat_ids, context=context):
                existing_search = sales_team_pool.search(
                cr, uid, [('analytic_account_id', '=', analytic_obj.id),
                          ('product_cat_id', '=', product_cat_obj.id)], context=context)
                if existing_search:
                    existing_counter +=1
                    continue
                sales_team_pool.create(cr, uid, {'analytic_account_id': analytic_obj.id,
                                                'product_cat_id': product_cat_obj.id,
                                                'sales_team_id': view_id and view_id[0] or False,
                                                }, context=context)
                created_counter +=1
        total = existing_counter + created_counter
        self.write(cr, uid, ids, {'state': 'generated',
                                  'existing_generated': existing_counter,
                                  'new_create': created_counter,
                                  'total': total,
                                 }, context=context)
        return {
            'name': _('Generate Sales Team Mapping'),
            'type': 'ir.actions.act_window',
            'res_model': 'generate.mapping',
            'res_id': ids and ids[0],
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': context,
            'nodestroy': True,
            }

generate_mapping()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
