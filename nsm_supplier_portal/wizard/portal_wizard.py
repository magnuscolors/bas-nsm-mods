# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

WELCOME_EMAIL_SUBJECT = _("Your OpenERP account at %(company)s")
WELCOME_EMAIL_BODY = _("""Dear %(name)s,

You have been given access to %(portal)s.

Your login account data is:
Database: %(db)s
Username: %(login)s

In order to complete the signin process, click on the following url:
%(url)s

%(welcome_message)s

--
OpenERP - Open Source Business Applications
http://www.openerp.com
""")

class wizard_user(osv.osv_memory):
    _inherit = 'portal.wizard.user'

    _columns = {

    }
    
    def _send_email(self, cr, uid, wizard_user, context=None):
        """ send notification email to a new portal user
            @param wizard_user: browse record of model portal.wizard.user
            @return: the id of the created mail.mail record
        """
        print '9999999999999999999999999999999999999'
        this_context = context
        ir_model_data = self.pool.get('ir.model.data')
        this_user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context)
        print 'uuuuuuuuuuuuuuuuuuuuuu',this_user
        if not this_user.email:
            raise osv.except_osv(_('Email Required'),
                _('You must have an email address in your User Preferences to send emails.'))

        # determine subject and body in the portal user's language
        user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
        print 'jljoiudfadoifuoifdfjkldsfsio',user
        context = dict(this_context or {}, lang=user.lang)
        template_id = False
        template_id = self.pool.get('ir.model.data').get_object(
                    cr, uid, 'nsm_supplier_portal', 'send_invitation_email')
        ctx = context.copy()
        print 'cccccccccccccccccccccccc', ctx
        print 'template _id',template_id
        
        #mail_mail = self.pool.get('mail.compose.message')
        mail_mail = self.pool.get('mail.mail')
        data = {
            'company': this_user.company_id.name,
            'portal': wizard_user.wizard_id.portal_id.name,
            'welcome_message': wizard_user.wizard_id.welcome_message or "",
            'db': cr.dbname,
            'name': user.name,
            'login': user.login,
            'url': user.signup_url,
        }
        mail_values = {
            'email_from': this_user.email,
            'email_to': user.email,
            'subject': template_id.subject ,#_(WELCOME_EMAIL_SUBJECT) % data,
            'body_html': template_id.body_html,#'<pre>%s</pre>' % (_(WELCOME_EMAIL_BODY) % data),
            'state': 'outgoing',
            'type': 'email',
        }
        mail_template_pool.send_mail(
                    new_cr, user, template_id=template_id, res_id=False,
                    force_send=True, context=ctx)
        
        mail_id = mail_mail.create(cr, uid, mail_values, context=this_context)
        ####
        mail_template_pool = self.pool.get('email.template')
        mail_template_pool.send_mail(
                    new_cr, user, template_id=template_id, res_id=False,
                    force_send=True, context=ctx)
                    
        ####                    
#        values = mail_mail.default_get(cr, uid, [], context=ctx)
        print 'lllllllllllllllllllllllllllllllllllllllllllll'
        return mail_mail.send(cr, uid, [mail_id], context=this_context)
        #return mail_mail.create(cr, uid, {}, context=ctx)

wizard_user()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
