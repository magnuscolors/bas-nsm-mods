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


class base_config_settings(osv.osv_memory):
    _inherit = 'base.config.settings'

    _columns = {
        'data_fname': fields.char('File Name'),
        'supplier_terms': fields.binary("Upload Supplier Invoice Reuse-authorization File"),
    }

    def execute(self, cr, uid, ids, context=None):
        result = super(base_config_settings, self).execute(
            cr, uid, ids, context=context)
        config = self.browse(cr, uid, ids[0], context)
        if config.supplier_terms:
            company_id = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.id
            self.pool.get('res.company').write(cr, uid, company_id, {
                'supplier_terms': config.supplier_terms,
                'data_fname': config.data_fname
            }, context=context)
        return result
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
