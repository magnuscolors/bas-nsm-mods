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

class account_analytic(osv.osv):
    _inherit = 'account.analytic.account'
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        if isinstance(ids, (int, long)):
            ids = [ids]
        for id in ids:
            elmt = self.browse(cr, uid, id, context=context)
            res.append((id, elmt.name))
        return res

    _columns = {
        'portal_main': fields.boolean('Portal Main'),
        'portal_sub': fields.boolean('Portal Sub'),
    }

    def onchange_portal(self, cr, uid, ids, portal_main, portal_sub, field,
                        context={}):
        if portal_main and portal_sub:
            return {'warning': {
                'title': _('Portal Warning!'),
                'message': _('You can not use same analytic account for '
                             'Main portal as well as Sub portal')},
                'value': {field:False
                          }
            }
        return {}
account_analytic()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
