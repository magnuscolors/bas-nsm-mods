# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class sales_team(osv.osv):
    _name = 'sales.team'
    _description = 'Sales Team'

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account',
                                               'Analytic Account'),
        'sale_person_id': fields.many2one('res.users', 'Sales Person',),
        'product_cat_id': fields.many2one('product.category',
                                          'Product Category',),
    }

    _sql_constraints = [
        ('analytic_prodt_cat_id_uniq', 'unique (analytic_account_id, product_cat_id)',
         'The combination of Analytic account and Product Category must be unique!'),
        ]

sales_team()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
