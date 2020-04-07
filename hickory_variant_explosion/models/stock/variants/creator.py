# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductVariantCreator(models.TransientModel):
    """
    The ProductVariantCreator class is meant to be used as a wizard where a user has the ability
    to generate variants for a specific template. It will include a few options where they can selectively
    choose which variants to generate instead of creating all permutations of the template attributes.
    """
    _name = 'product.variant.creator'

    template_id = fields.Many2one(comodel_name='product.template', string='Product Template')
    template_name = fields.Char(related='template_id.name')
    method = fields.Selection(string='Creation Method', required=True, selection=[
        ('all', 'All Combinations'),
        ('selective', 'Selective')])
    matrix_line_ids = fields.One2many(comodel_name='product.variant.matrix.line', inverse_name='creator_id', string='Matrix Lines')

    @api.multi
    def run(self):
        """
        Run the variant creation process based on the selection parameters.

        :return: None
        """
        self.ensure_one()

        values = self.matrix_line_ids.mapped('value_ids')
        if len(values) < 3:
            raise ValidationError(_('Select at least three attribute values to create multiple combinations!'))

        try:
            getattr(self, 'run_{}'.format(self.method))()
        except Exception:
            raise UserError(_('Sorry, there was a problem creating these variants. Contact your administrator for more information.'))

    @api.multi
    def run_all(self):
        """
        Run the product variant creator using the "All Combinations" method.

        :return: None
        """
        self.ensure_one()

        self.template_id._create_variant_ids()
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'product.template',
                'domain': [('id', '=', self.template_id.id)]}

    @api.multi
    def run_selective(self):
        """
        Run the product variant creator using the "Selective" method.

        :return:
        """
        self.ensure_one()

        self.template_id.create_partial_variant_ids([matrix_line.value_ids for matrix_line in self.matrix_line_ids if matrix_line.value_ids], drop=False)
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'product.template',
                'domain': [('id', '=', self.template_id.id)]}

    def populate_matrix(self):
        """
        Helper method to fill out the initial matrix. This will only be used if the user selects to generate
        variants with the Selective method.

        This method is meant to be used before creation so the user can modify the matrix if needed.

        :return: self
        """
        matrix_line_pool = self.env['product.variant.matrix.line']
        for attribute_line in self.template_id.attribute_line_ids:
            value_ids = [(4, val) for val in attribute_line.value_ids.ids]
            matrix_line_pool.create({'attribute_id': attribute_line.attribute_id.id,
                                     'creator_id': self.id,
                                     'use': 'all_values',
                                     'value_ids': value_ids,
                                    })
        return self
