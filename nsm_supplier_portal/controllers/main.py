# -*- coding: utf-8 -*-

import base64
import simplejson
from openerp.tools.translate import _
from openerp.addons.web import http
openerpweb = http
import urllib2
from web.controllers.main import Binary
#----------------------------------------------------------
# OpenERP Binary saveas_ajax improved
#----------------------------------------------------------
def content_disposition(filename, req):
    filename = filename.encode('utf8')
    escaped = urllib2.quote(filename)
    browser = req.httprequest.user_agent.browser
    version = int((req.httprequest.user_agent.version or '0').split('.')[0])
    if browser == 'msie' and version < 9:
        return "attachment; filename=%s" % escaped
    elif browser == 'safari':
        return "attachment; filename=%s" % filename
    else:
        return "attachment; filename*=UTF-8''%s" % escaped

class ImprovedBinary(Binary):
    _cp_path = "/web/binary"

    @openerpweb.httprequest
    def saveas_ajax(self, req, data, token):
        jdata = simplejson.loads(data)
        model = jdata['model']
        field = jdata['field']
        data = jdata['data']
        id = jdata.get('id', None)
        filename_field = jdata.get('filename_field', None)
        context = jdata.get('context', {})

        Model = req.session.model(model)
        fields = [field]
        if filename_field:
            fields.append(filename_field)
        if data:
            res = { field: data }
            #BIZZ Fix for the getting proper file name from default
            res_file_name = Model.default_get([filename_field], context)
            res.update(res_file_name)
        elif id:
            res = Model.read([int(id)], fields, context)[0]
        else:
            res = Model.default_get(fields, context)
        filecontent = base64.b64decode(res.get(field, ''))
        if not filecontent:
            raise ValueError(_("No content found for field '%s' on '%s:%s'") %
                (field, model, id))
        else:
            filename = '%s_%s' % (model.replace('.', '_'), id)
            if filename_field:
                filename = res.get(filename_field, '') or filename
            return req.make_response(filecontent,
                headers=[('Content-Type', 'application/octet-stream'),
                        ('Content-Disposition', content_disposition(filename, req))],
                cookies={'fileToken': token})

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
