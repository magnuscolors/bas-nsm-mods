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

from openerp.osv import osv, orm, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

class wizard_user(orm.TransientModel):
    _inherit = 'portal.wizard.user'

    def action_apply(self, cr, uid, ids, context=None):
        for wiz_user in self.browse(cr, SUPERUSER_ID, ids, context):
            if wiz_user.in_portal:
                partner = wiz_user.partner_id
                if not partner.product_category_ids:
                    raise orm.except_orm(_('No Categories defined for %s' % partner.name),
                    _('For this supplier to be invited to the Portal you have to grant him one or more Invoice Categories and one or more Titles/Departments.'))
                if not partner.analytic_account_ids:
                    if not partner.product_price_ids:
                       raise orm.except_orm(_('No Titles/Departments/Prices defined for %s' % partner.name),
                       _('For this supplier to be invited to the Portal you have to grant him one or more Invoice Categories and one or more Titles/Departments/Prices.'))
        return super(wizard_user, self).action_apply(cr, uid, ids, context=context)