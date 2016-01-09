from openerp.osv import osv


class account_move_line(osv.osv):
    _inherit = 'account.move.line'

    def default_get(self, cr, uid, fields, context=None):
        data = self._default_get_custom(cr, uid, fields, context=context)
        for f in data.keys():
            if f not in fields:
                del data[f]
        return data
    def _default_get_custom(self, cr, uid, fields, context=None):
        #default_get should only do the following:
        #   -propose the next amount in debit/credit in order to balance the move
        #   -propose the next account from the journal (default debit/credit account) accordingly
        if context is None:
            context = {}
        account_obj = self.pool.get('account.account')
        period_obj = self.pool.get('account.period')
        journal_obj = self.pool.get('account.journal')
        move_obj = self.pool.get('account.move')
        tax_obj = self.pool.get('account.tax')
        fiscal_pos_obj = self.pool.get('account.fiscal.position')
        partner_obj = self.pool.get('res.partner')
        currency_obj = self.pool.get('res.currency')

        if not context.get('journal_id', False):
            context['journal_id'] = context.get('search_default_journal_id', False)
        if not context.get('period_id', False):
            context['period_id'] = context.get('search_default_period_id', False)
        context = self.convert_to_period(cr, uid, context)

        # Compute simple values
        data = super(account_move_line, self).default_get(cr, uid, fields, context=context)
        if context.get('journal_id'):
            total = 0.0
            #in account.move form view, it is not possible to compute total debit and credit using
            #a browse record. So we must use the context to pass the whole one2many field and compute the total
            if context.get('line_id'):
                for move_line_dict in move_obj.resolve_2many_commands(cr, uid, 'line_id', context.get('line_id'), context=context):
                    data['name'] = data.get('name') or move_line_dict.get('name')
                    #changes for the module
                    data['analytic_account_id'] = data.get('analytic_account_id') or move_line_dict.get('analytic_account_id', False)
                    #changes Ends
                    data['partner_id'] = data.get('partner_id') or move_line_dict.get('partner_id')
                    total += move_line_dict.get('debit', 0.0) - move_line_dict.get('credit', 0.0)
            elif context.get('period_id'):
                #find the date and the ID of the last unbalanced account.move encoded by the current user in that journal and period
                move_id = False
                cr.execute('''SELECT move_id, date FROM account_move_line
                    WHERE journal_id = %s AND period_id = %s AND create_uid = %s AND state = %s
                    ORDER BY id DESC limit 1''', (context['journal_id'], context['period_id'], uid, 'draft'))
                res = cr.fetchone()
                move_id = res and res[0] or False
                data['date'] = res and res[1] or period_obj.browse(cr, uid, context['period_id'], context=context).date_start
                data['move_id'] = move_id
                if move_id:
                    #if there exist some unbalanced accounting entries that match the journal and the period,
                    #we propose to continue the same move by copying the ref, the name, the partner...
                    move = move_obj.browse(cr, uid, move_id, context=context)
                    data.setdefault('name', move.line_id[-1].name)
                    #changes for the module
                    data.setdefault('analytic_account_id', move.line_id[-1].analytic_account_id.id)
                    #changes Ends
                    for l in move.line_id:
                        data['partner_id'] = data.get('partner_id') or l.partner_id.id
                        data['ref'] = data.get('ref') or l.ref
                        total += (l.debit or 0.0) - (l.credit or 0.0)

            #compute the total of current move
            data['debit'] = total < 0 and -total or 0.0
            data['credit'] = total > 0 and total or 0.0
            #pick the good account on the journal accordingly if the next proposed line will be a debit or a credit
            journal_data = journal_obj.browse(cr, uid, context['journal_id'], context=context)
            account = total > 0 and journal_data.default_credit_account_id or journal_data.default_debit_account_id
            #map the account using the fiscal position of the partner, if needed
            part = data.get('partner_id') and partner_obj.browse(cr, uid, data['partner_id'], context=context) or False
            if account and data.get('partner_id'):
                account = fiscal_pos_obj.map_account(cr, uid, part and part.property_account_position or False, account.id)
                account = account_obj.browse(cr, uid, account, context=context)
            data['account_id'] =  account and account.id or False
            #compute the amount in secondary currency of the account, if needed
            if account and account.currency_id:
                data['currency_id'] = account.currency_id.id
                #set the context for the multi currency change
                compute_ctx = context.copy()
                compute_ctx.update({
                        #the following 2 parameters are used to choose the currency rate, in case where the account
                        #doesn't work with an outgoing currency rate method 'at date' but 'average'
                        'res.currency.compute.account': account,
                        'res.currency.compute.account_invert': True,
                    })
                if data.get('date'):
                    compute_ctx.update({'date': data['date']})
                data['amount_currency'] = currency_obj.compute(cr, uid, account.company_id.currency_id.id, data['currency_id'], -total, context=compute_ctx)
        data = self._default_get_move_form_hook(cr, uid, data)
        return data
    def _default_get_move_form_hook(self, cursor, user, data):
        '''Called in the end of default_get method for manual entry in account_move form'''
    #   if data.has_key('analytic_account_id'):
    #       del(data['analytic_account_id'])
        if data.has_key('account_tax_id'):
            del(data['account_tax_id'])
        return data
account_move_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
