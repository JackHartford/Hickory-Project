# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.misc import ustr
from odoo.addons.auth_signup.models.res_users import SignupError

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _create_user_from_template(self, values):
        template_user_id = literal_eval(self.env['ir.config_parameter'].sudo().get_param('base.template_portal_user_id', 'False'))
        template_user = self.browse(template_user_id)
        print("Testing name string", values)
        values.update({'name':values.get('email')})
        print("Testing email string", values)

        if not template_user.exists():
            raise ValueError(_('Signup: invalid template user'))

        if not values.get('login'):
            raise ValueError(_('Signup: no login given for new user'))
        if not values.get('partner_id') and not values.get('name'):
            raise ValueError(_('Signup: no name or partner given for new user'))

        # create a copy of the template user (attached to a specific partner_id if given)
        values['active'] = True
        values['customer'] = True
        try:
            with self.env.cr.savepoint():
                return template_user.with_context(no_reset_password=True).copy(values)
        except Exception as e:
            # copy may failed if asked login is not available.
            raise SignupError(ustr(e))