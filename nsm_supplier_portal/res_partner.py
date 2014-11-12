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


class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'user_create': fields.boolean('User is created'),
    }
    
    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """

        res = {}
        res = super(res_partner, self).fields_view_get(cr, user, view_id, view_type,
                                                       context, toolbar=toolbar, submenu=submenu)
        if not context.get('is_portal'):
            return res
        res['toolbar'] = {'print': [], 'other':[]}
        return res

    '''
    def create_supplier_user(self, cr, uid, ids, context={}):
        if not context:
            context = {}
        partner_ids = []
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.user_create:
                continue
            user_pool = self.pool.get('res.users')
            user_ids = user_pool.search(cr, uid, [('name', '=', obj.name)], context=context)
            if user_ids:
                raise osv.except_osv(_('Error!'), _('%s user is already created' % obj.name))
            login_name = ''.join(e for e in obj.name if e.isalnum())
            user_id = user_pool.create(cr, uid, {
                'login': login_name,
                'partner_id': obj.id,
                'tz': context['tz']
            }, context=context)
            partner_ids.append(user_id)
            self.write(cr, uid, obj.id, {
                'user_create': True,
            }, context=context)
        user_pool.action_reset_password(cr, uid, partner_ids, context)
    '''

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
