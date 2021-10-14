from odoo import api, fields, models


class GYMInfo(models.Model):
    _name = 'gym.info'

    name = fields.Char('Name',required=True)
    middle_name = fields.Char('Middle Name')
    mobile = fields.Integer('mobile')
    city = fields.Char('City', default='Mumbai', readonly =True)
    gender_male = fields.Selection([('male', 'Male'),
                                    ('female', 'Female')],
                                      'Gender', required=True)
    is_pwd = fields.Boolean('Is Phycially Handiacpped?')


