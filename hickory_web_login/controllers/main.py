from odoo import http, models, fields, _
from odoo.http import request, route
from odoo.addons.portal.controllers.web import Home
from odoo.addons.portal.controllers.portal import CustomerPortal

class Website(Home):

    # ------------------------------------------------------
    # Login - overwrite of the web login so that regular users are redirected to the backend
    # while portal users are redirected to the frontend by default
    # ------------------------------------------------------

    @http.route(website=True, auth="public")
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(redirect=redirect, *args, **kw)
        print(response,request.uid, "Testing")
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/my/account'
            print(redirect)
            return http.redirect_with_hash(redirect)
        return response

class CustomCustomerPortal(CustomerPortal):

    
    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        redirect="/shop"
        return super(CustomCustomerPortal, self).account(redirect=redirect,**post)