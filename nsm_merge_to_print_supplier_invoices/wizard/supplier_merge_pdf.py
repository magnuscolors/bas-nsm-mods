# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Odoo Experts
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

import base64
import StringIO
import pyPdf
from openerp import netsvc

class supplier_invoice_merge_pdf(osv.osv_memory):
    _name = 'supplier.invoice.merge.pdf'
    _description = 'Supplier Invoice Merge PDF'

    def _get_file_data(self, cr, uid, context={}):
        invoice_ids = context.get('active_ids',[])
        if not invoice_ids:
            return False
        final_pdf = []
        att_pool = self.pool['ir.attachment']
        output = pyPdf.PdfFileWriter()
        for invoice in self.pool['account.invoice'].browse(cr, uid, invoice_ids, context=context):
            flg = False
            att_ids = att_pool.search(cr ,uid, [('res_model', '=', 'account.invoice'),
                                       ('res_id', '=', invoice.id)])
            for att_data in att_pool.browse(cr, uid, att_ids, context=context):
                if 'PDF' not in att_data.file_type.upper() :
                    continue
                if att_data.datas_fname and att_data.datas and att_data.datas_fname.split(".")[-1].upper() == "PDF":
                    data = base64.decodestring(att_data.datas)
                    buffer_file = StringIO.StringIO(data)
                    input_attachment = pyPdf.PdfFileReader(buffer_file)
                    flg = True
                    for page in range(input_attachment.getNumPages()):
                        output.addPage(input_attachment.getPage(page))
            if not flg:
                ctx = context.copy()
                ctx['model'] = 'account.invoice'
                report_service = 'report.blank.invoice.report'
                service = netsvc.LocalService(report_service)
                (result, format) = service.create(
                    cr, uid, [invoice.id],
                    {'model': 'account.invoice'}, context=ctx)
                buffer_file = StringIO.StringIO(result)
                input_report = pyPdf.PdfFileReader(buffer_file)
                for page in range(input_report.getNumPages()):
                    output.addPage(input_report.getPage(page))

        outputStream = StringIO.StringIO()
        output.write(outputStream)
        res =  outputStream.getvalue().encode('base64')
        outputStream.close()
        return res




    _columns = {
        'file_data' : fields.binary('Merged PDF'),
        'file_name' : fields.char('File Name')
    }
    _defaults = {
        'file_name': 'Invoice Merged Attachments.pdf',
        'file_data': _get_file_data
    }

supplier_invoice_merge_pdf()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
