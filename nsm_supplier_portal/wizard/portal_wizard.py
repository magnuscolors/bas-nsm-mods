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
from openerp import SUPERUSER_ID

class wizard_user(osv.osv_memory):
    _inherit = 'portal.wizard.user'
    
    def _send_email(self, cr, uid, wizard_user, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """
        this_context = context
        this_user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)
        if not this_user.email:
            raise osv.except_osv(_('Email Required'),
                _('You must have an email address in your User Preferences to send emails.'))

        template_id = False
        template_id = self.pool.get('ir.model.data').get_object(
                    cr, uid, 'nsm_supplier_portal', 'send_invitation_email')
        ctx = context.copy()
        mail_template_pool = self.pool.get('email.template')
        mail_template_pool.send_mail(
                    cr, uid, template_id=template_id, res_id=wizard_user.partner_id.id,
                    force_send=True, context=ctx)
        
        return True

wizard_user()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
