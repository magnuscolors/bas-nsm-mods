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

from openerp.osv import osv, orm, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

class wizard_user(orm.TransientModel):
    _inherit = 'portal.wizard.user'
    
    def _send_email(self, cr, uid, wiz_user, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """
        user = self._retrieve_user(cr, SUPERUSER_ID, wiz_user, context)
        if ("nsm_supplier_portal.group_module_supplier_portal_user",'in', [x.get_xml_id(x.id) for x in user.groups_id]):
            this_context = context
            context = dict(this_context or {}, lang=user.lang)
            template_id = False
            template_id = self.pool.get('ir.model.data').get_object(
                    cr, uid, 'nsm_supplier_portal', 'send_invitation_email')
            ctx = context.copy()
            mail_template_pool = self.pool.get('email.template')
            return mail_template_pool.send_mail(cr, uid, template_id=template_id, res_id=wiz_user.partner_id.id, force_send=True, context=ctx)
        return super(wizard_user, self)._send_email(cr, uid, wiz_user, context=None)

wizard_user()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
