import re
from datetime import date
from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rent = fields.Boolean('Can be Rented', default='True')
    rent_price = fields.Integer('Rent Price')


class gymschedule(models.Model):
    # _name = 'gym.schedule'
    _inherit = 'res.partner'
    joining_date = fields.Date('Joining Date')
    workout_ids = fields.One2many(comodel_name='workout.info', inverse_name='workout_id')
    total_amount = fields.Integer('Total amount', compute='_total',readonly= True)

    @api.depends('workout_ids')
    def _total(self):
        total = 0
        for record in self.workout_ids:
            total += record.price
        self.total_amount = total


class WorkoutInfo(models.Model):
    _name = 'workout.info'
    name = fields.Char('name')
    exercise = fields.Char('exercise')
    hours = fields.Integer('hours')
    massage = fields.Boolean('massage')
    supplementary = fields.Boolean('supplementary')
    price = fields.Integer('price', compute='_compute_price', store=True)
    # total_price= fields.Integer('total_price', compute= '_compute_total_price', readonly= True)
    workout_id = fields.Many2one(comodel_name='res.partner')
    sets_id = fields.Many2one(comodel_name='sets.info')


    @api.depends('massage', 'supplementary', 'price')
    def _compute_price(self):
        mprice = 500
        sprice = 100
        if self.massage == True and self.supplementary == True:
            self.price = mprice + sprice
        elif self.massage:
            self.price = mprice
        elif self.supplementary:
            self.price = sprice
        else:
            self.price = 0



class sets(models.Model):
    _name = 'sets.info'
    exercise_name = fields.Char('exercise name')
    sets = fields.Char('sets')
    reps = fields.Char('reps')

#
# class account(models.Model):
#     _inherit = 'account.move'
#     partner_id = fields.Many2one(comodel_name='res.partner')


# class company(models.Model):
#     _inherit = 'res.partner'
#     company_type = fields.Selection([('person', 'Individual'),
#                                      ('company', 'Company')], 'Company Type')

# class product(models.Model):
#     _inherit = 'purchase.order'
#
#     def product(self):
#         if self.product_qty > 20:
#             # raise .ValidationError('Not valid message')
#         else:



class Product(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty')
    def _check_something(self):
        for record in self:
            if record.product_qty > 20:
                raise UserError(("Your product quantity is grater than 20 : %s" % record.product_qty))


class CompanyInfo(models.Model):
    _inherit = 'sale.order'

    company_check = fields.Boolean('Company check')

    @api.onchange('partner_id')
    def company_info(self):
        print('company')
        if self.partner_id.is_company == True:
            self.company_check = True
        else:
            self.company_check = False


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print('its working')
        return res

class payment(models.Model):
    _inherit = 'sale.order'

    @api.model
    def action_confirm(self):
        self.payment_term_id.id = 1

    

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    ci_product = fields.Selection([('person', 'Individual'),('company', 'Company')],'Company or Individual',related='partner_id.company_type')



class ProductProduct(models.Model):
    _inherit = 'product.product'
    ci_product = fields.Selection([('person', 'Individual'),
                                   ('company', 'Company')], 'Company or Individual', )



class BirthDate(models.Model):
    _inherit = 'res.partner'

    dob = fields.Date('Birthdate')
    age = fields.Integer('Age',readonly=1)

    @api.onchange('dob')
    def _calculate_age(self):
        today = date.today()
        self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return 0


class EmailValidation(models.Model):
    _inherit = 'res.partner'

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+([a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')



