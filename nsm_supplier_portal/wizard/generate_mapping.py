# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class generate_mapping(osv.osv_memory):
    _name = 'generate.mapping'
    _description = 'Generate Sales Team Mapping'

    _columns = {
        'state': fields.selection([('draft', 'Draft'),
                                   ('generated', 'Generated')],
                                  'State',),
        'existing_generated': fields.integer('Existing',),
        'new_create': fields.integer('New Created'),
        'total': fields.integer('Total'),

    }
    _defaults = {
        'state': 'draft',
    }

    def generate_mapping(self, cr, uid, ids, context={}):
        analytic_ac_pool = self.pool.get('account.analytic.account')
        product_category_pool = self.pool.get('product.category')
        sales_team_pool = self.pool.get('sales.team')
        crm_sales_pool = self.pool.get('crm.case.section')
        existing_counter = 0
        created_counter = 0
        total = 0

        analytic_search_ids = analytic_ac_pool.search(
            cr, uid, [('portal_main', '=',  True)], context=context)
        product_cat_ids = product_category_pool.search(
            cr, uid, [], context=context)

        view_ref = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'nsm_supplier_portal', 'section_sales_department1')
        view_id = view_ref and view_ref[1] or False,

        for analytic_obj in analytic_ac_pool.browse(cr, uid,
                                                    analytic_search_ids,
                                                    context=context):
            for product_cat_obj in product_category_pool.browse(
                cr, uid, product_cat_ids, context=context):

                existing_search = sales_team_pool.search(
                    cr, uid, [('analytic_account_id', '=', analytic_obj.id),
                              ('product_cat_id', '=', product_cat_obj.id)], context=context)
                if existing_search:
                    existing_counter +=1
                    continue
                sales_team_pool.create(
                    cr, uid,
                    {'analytic_account_id': analytic_obj.id,
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
