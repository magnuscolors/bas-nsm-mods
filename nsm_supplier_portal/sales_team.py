# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class sales_team(osv.osv):
    _name = 'sales.team'
    _description = 'Sales Team Mapping'
    _rec_name = 'name'

    def concate_name(self, cr, uid, ids, name, args=None, context={}):
        """concate name of product category and analytic account"""
        result = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            result[self_obj.id] = self_obj.analytic_account_id.name.strip() + ' / ' + self_obj.product_cat_id.name.strip()
        return result

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
        'product_cat_id': fields.many2one('product.category',
                                          'Product Category',),
        'name': fields.function(concate_name,
                                string='Name', type='char',
                                store=True, size=64),
        # 'sales_team_id': fields.many2one('crm.case.section', 'Sales Team',),

        'sales_team_id': fields.many2one('crm.team', 'Sales Team',),
    }

    _sql_constraints = [
        ('analytic_prodt_cat_id_uniq', 'unique (analytic_account_id, product_cat_id)',
         'The combination of Analytic account and Product Category must be unique!'),
        ]

sales_team()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
