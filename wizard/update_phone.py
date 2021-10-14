from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError

import re


class CustomerWizard(models.TransientModel):
    _name = "customer.wizard"
    _description = "Customer Wizard"

    update_phone = fields.Char('Update Phone')

    def phone_update(self):

        active_id = self.env.context.get('active_id')
        customer_info_rec = self.env['res.partner']
        customer_change_id = customer_info_rec.search([('id', '=', active_id)])
        print("active_id>>>>", active_id)
        print('customer_info>>', customer_info_rec)
        print('customer_change_id>>>', customer_change_id)
        customer_change_id.phone = self.update_phone

        pattern = re.compile("(0|91)?[7-9][0-9]{9}")
        if pattern.match(str(self.update_phone)) and (len(self.update_phone) <= 10):
            customer_change_id.phone = self.update_phone
        else:
            raise ValidationError("Phone number length must be 10 digit only")
        return 1