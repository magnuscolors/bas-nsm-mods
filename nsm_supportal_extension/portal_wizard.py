# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2016 Magnus
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

from openerp.osv import orm
from openerp.osv import fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID




class wizard_user(orm.TransientModel):
    _inherit = 'portal.wizard.user'

    def action_apply(self, cr, uid, ids, context=None):
        for wizard_user in self.browse(cr, SUPERUSER_ID, ids, context):
            portal = wizard_user.wizard_id.portal_id
            partner = wizard_user.partner_id
            user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
            if wizard_user.in_portal:
                if not partner.product_category_ids:
                    raise orm.except_orm(_('No Categories defined for %s' % partner.name),
                    _('For this supplier to be invited to the Portal you have to grant him one or more Invoice Categories and one or more Titles/Departments.'))
                if not partner.analytic_account_ids:
                    raise orm.except_orm(_('No Titles/Departments defined for %s' % partner.name),
                    _('For this supplier to be invited to the Portal you have to grant him one or more Invoice Categories and one or more Titles/Departments.'))
                # create a user if necessary, and make sure it is in the portal group
                if not user:
                    user = self._create_user(cr, SUPERUSER_ID, wizard_user, context)
                if (not user.active) or (portal not in user.groups_id):
                    user.write({'active': True, 'groups_id': [(4, portal.id)]})
                    # prepare for the signup process
                    user.partner_id.signup_prepare()
                    wizard_user = self.browse(cr, SUPERUSER_ID, wizard_user.id, context)
                    self._send_email(cr, uid, wizard_user, context)
            else:
                # remove the user (if it exists) from the portal group
                if user and (portal in user.groups_id):
                    # if user belongs to portal only, deactivate it
                    if len(user.groups_id) <= 1:
                        user.write({'groups_id': [(3, portal.id)], 'active': False})
                    else:
                        user.write({'groups_id': [(3, portal.id)]})