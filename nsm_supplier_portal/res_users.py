# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
from datetime import datetime, timedelta


def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

class res_users(osv.Model):
    _inherit = 'res.users'

    _columns = {

    }

    def action_reset_password(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id for user in self.browse(cr, uid, ids, context)]
        res_partner.signup_prepare(
            cr, uid, partner_ids, signup_type="reset", expiration=now(days=+1), context=context)

        if not context:
            context = {}

        # send email to users with their signup url
        template = False
        if context.get('create_user'):
            try:
                template = self.pool.get('ir.model.data').get_object(
                    cr, uid, 'nsm_supplier_portal', 'send_invitation_email')
            except ValueError:
                pass
        if not bool(template):
            template = self.pool.get('ir.model.data').get_object(
                cr, uid, 'auth_signup', 'reset_password_email')
        mail_obj = self.pool.get('mail.mail')
        assert template._name == 'email.template'
        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise osv.except_osv(
                    _("Cannot send email: user has no email address."), user.name)
            mail_id = self.pool.get('email.template').send_mail(
                cr, uid, template.id, user.id, True, context=context)
            mail_state = mail_obj.read(cr, uid, mail_id, ['state'], context=context)
            if mail_state and mail_state['state'] == 'exception':
                raise osv.except_osv(
                    _("Cannot send email: no outgoing email server configured.\nYou can configure it under Settings/General Settings."), user.name)
            else:
                return True
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
