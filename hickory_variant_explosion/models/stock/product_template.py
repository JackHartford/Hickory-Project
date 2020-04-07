# -*- coding: utf-8 -*-
import itertools
from odoo import _, api, fields, models
from odoo.addons.product.models.product_template import ProductTemplate as BaseTemplate


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    attribute_count = fields.Integer(string='Attribute Count', compute='_compute_attribute_count', store=True)
    has_variants = fields.Boolean(string='Has Variants', compute='_compute_has_variants',
                                  help='A true / false value that indicates if this product template has any variants associated with it.'
                                       'If it has no variants, then users will not be able to buy, sell, or move the product.')
    real_sales_count = fields.Integer(compute='_compute_sales_count', string="# Sales", store=False)
    real_purchase_count = fields.Integer(compute='_compute_purchase_count', string='# Purchases', store=False)
    sales_count = fields.Integer(related='real_sales_count')
    purchase_count = fields.Integer(related='real_purchase_count')
    all_product_variant_ids = fields.Many2many(comodel_name='product.product', compute='_compute_all_variants')
    mandatory_product_ids = fields.Many2many('product.template', 'rel_table_mandatory_product_ids', 'src_id', 'dest_id',
                                              string='Mandatory Products')

    @api.multi
    def _compute_has_variants(self):
        """
        Compute if there are any product.product records for this template. We are going to search, with a limit=1, to
        see if there is at least one record. We don't care if there is more than 1, as long as there is at least 1.

        :return: None
        """
        for template in self:
            template.has_variants = len(self.env['product.product'].search([('product_tmpl_id', '=', self.id)], limit=1)) >= 1

    @api.multi
    @api.depends('attribute_line_ids')
    def _compute_attribute_count(self):
        """
        Compute the total number of variant attributes for a set of templates. This field is used to filter out views / button
        actions if variant attributes aren't relevant.

        :return: None
        """
        for template in self:
            template.attribute_count = len(template.attribute_line_ids)

    @api.multi
    def create_variant_ids(self):
        """
        We are going to force an override of the `create_variant_ids` function from
        the parent class so that we can ignore all out of the box generation of multiple variants.
        Essentially this is just going to disable automatic variant creation across the board
        to avoid any confusion, except for individual template. Individual templates will still generate
        an individual variant that can be used for other operations in the system.

        The original `create_variant_ids` functionality is not 100% lost since we are copying it into
        another function below where we can use it ourselves where needed.

        :return: None
        """
        for template in self:
            if not template.attribute_line_ids:
                super(ProductTemplate, template).create_variant_ids()

    @api.multi
    def _create_variant_ids(self):
        """
        This function will contain all of the original functionality of the `create_variant_ids` function
        from the parent class. You will see `pass` below because we are using a monkey patch at the bottom of
        this file to pull this functionality in. This is a required workaround to get around the _inherit functionality
        since we are overriding `create_variant_ids` above.

        WARNING: Do not actually write anything in this method block below since it will get overwritten with the monkey patch.

        :return: super.create_variant_ids()
        """
        pass

    @api.multi
    def create_partial_variant_ids(self, values, drop=True):
        """
        TODO: Figure out the best way to handle "Existing Variants" if we want to try to keep them instead
        of dropping every single time.

        :param values:
        :param drop:
        :return:
        """
        self.ensure_one()

        attribute_value_pool = self.env['product.attribute.value']
        do_not_include = []
        value_permutations = itertools.product(*(value_ids.ids for value_ids in values if value_ids and value_ids[:1].attribute_id.create_variant))
        variant_matrix = [attribute_value_pool.browse(value_ids) for value_ids in value_permutations]
        existing_variants = []
        to_create_variants = [value_ids for value_ids in variant_matrix if set(value_ids.ids) not in existing_variants]

        for variant_ids in to_create_variants:
            variant = self.env['product.product'].create({'product_tmpl_id': self.id, 'attribute_value_ids': [(6, 0, variant_ids.ids)]})
            do_not_include.append(variant.id)

        if drop:
            self.action_drop_all_variants(do_not_include)

    @api.multi
    def action_drop_all_variants(self, do_not_include=[]):
        """
        A button action to delete all the variants for a given product. This will be used for variant management, in case
        a user would like to start over and regenerate the variants for a template from scratch.

        We will want to ensure that there is a frontend action somewhere that prompts the user for "Are you sure you really want
        to do this?" since there are no checks and balances here.

        :return: None
        """
        self.ensure_one()

        domain = [('product_tmpl_id', '=', self.id)]
        if do_not_include and type(do_not_include) == list:
            domain.append(('id', 'not in', do_not_include))
        self.env['product.product'].search(domain).update({'active': False})

    @api.multi
    def action_show_variant_creator(self):
        """
        A button action to open up the product variant creator. This is the wizard that will allow users to generate their
        own variants instead of the system auto generating them based on attributes.

        :return: dict A redirect action to open a new wizard form
        """
        self.ensure_one()
        creator_vals = {'template_id': self.id, 'method': 'selective'}
        creator = self.env['product.variant.creator'].create(creator_vals)
        creator.populate_matrix()

        return {'type': 'ir.actions.act_window',
                'name': _('Variant Creation'),
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'res_model': 'product.variant.creator',
                'res_id': creator.id, }

    @api.multi
    def update_counts(self):
        """
        A function that is meant to be used with a Server Action. This will allow us to create a function
        like "Recompute" or "Update Values" so that we can test or recompute existing products if needed.

        :return: None
        """
        self._compute_all_variants()
        self._compute_sales_count()
        self._compute_quantities()

    @api.multi
    def _compute_sales_count(self):
        """
        Compute the sales count. This not a direct inheritance from the parent function. I ran into issues with
        directly inheriting so we created a new field and make the original field related.

        :return: None
        """
        for template in self:
            sales_order_lines = self.env['sale.order.line'].search([('product_id', 'in', template.all_product_variant_ids.ids)])
            template.real_sales_count = len(sales_order_lines.mapped('order_id'))

    @api.multi
    def _compute_purchase_count(self):
        """
        Compute the purchase count. This not a direct inheritance from the parent function. I ran into issues with
        directly inheriting so we created a new field and make the original field related.

        :return: None
        """
        for template in self:
            purchase_order_lines = self.env['purchase.order.line'].search([('product_id', 'in', template.all_product_variant_ids.ids)])
            template.real_purchase_count = len(purchase_order_lines.mapped('order_id'))

    def _compute_quantities_dict(self):
        """
        Override the parent _compute_quantities_dict function so that we can reference all_product_variant_ids
        instead of the standard variant_ids. This will allow us to include inactive variants whenever we are calculating
        the counts for template views.

        :return: dict
        """
        variants_available = self.mapped('all_product_variant_ids')._product_available()
        prod_available = {}
        for template in self:
            qty_available = virtual_available = incoming_qty = outgoing_qty = 0
            for p in template.all_product_variant_ids:
                qty_available += variants_available[p.id]["qty_available"]
                virtual_available += variants_available[p.id]["virtual_available"]
                incoming_qty += variants_available[p.id]["incoming_qty"]
                outgoing_qty += variants_available[p.id]["outgoing_qty"]
            prod_available[template.id] = {"qty_available": qty_available,
                                           "virtual_available": virtual_available,
                                           "incoming_qty": incoming_qty,
                                           "outgoing_qty": outgoing_qty, }
        return prod_available

    @api.multi
    def _compute_all_variants(self):
        """
        Compute a list of variants including the inactive variants.

        :return: None
        """
        for template in self:
            template.all_product_variant_ids = self.env['product.product'].search([
                ('product_tmpl_id', '=', template.id), '|', ('active', '=', True), ('active', '=', False)])


# Monkey Patch Fun Times
ProductTemplate._create_variant_ids = BaseTemplate.create_variant_ids
