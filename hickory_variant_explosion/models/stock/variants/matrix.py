# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductVariantMatrix(models.TransientModel):
    """
    The ProductVariantMatrix is a table that is used to generate the variant matrix before individual
    product variants are created from a template. This allows users to have some insight / see the matrix
    of attributes before actually generating the variants themselves.
    """
    _name = 'product.variant.matrix.line'

    creator_id = fields.Many2one(comodel_name='product.variant.creator', string='Creator')
    attribute_id = fields.Many2one(comodel_name='product.attribute', string='Attribute')
    attribute_name = fields.Char(related='attribute_id.name')
    valid_values = fields.Many2many(comodel_name='product.attribute.value', compute='_compute_valid_values')
    use = fields.Selection(string='Use', selection=[
        ('all_values', 'All Values'),
        ('some_values', 'Some Values'),
        ('no_values', 'No Values'), ])
    value_ids = fields.Many2many(string='Values', comodel_name='product.attribute.value',
                                 relation='matrix_value_rel', column1='matrix_id', column2='value_id')

    @api.multi
    def _compute_valid_values(self):
        """
        :return: None
        """
        for line in self:
            line.valid_values = self.env['product.attribute.line'].search([
                ('attribute_id', '=', line.attribute_id.id),
                ('product_tmpl_id', '=', line.creator_id.template_id.id), ], limit=1).value_ids.ids

    @api.onchange('use')
    def onchange_use_setup_values(self):
        """
        Event listener to fire when `use` is changed. This method will update the values fields to ensure that
        they are filtered out correctly, contain the correct values, and are editable/not editable to the user
        based on the `use` method selection.

        :return: dict
        """
        self.env.context = self.with_context({'noset_use': True}).env.context

        if self.use == 'no_values':
            self.value_ids = [(6, 0, [])]
        if self.use == 'all_values':
            self.value_ids = [(6, 0, self.valid_values.ids)]

    @api.onchange('value_ids')
    def onchange_value_ids_update_use(self):
        """
        Event listener to fire when `value_ids` are changed. This method will flip the `use` field to Some Values whenever
        values are changed. This is a workaround so that we can make the values field readonly=False when All Values is selected, otherwise
        when the records saves it will not include the values since they are marked readonly.

        :return: None
        """
        if not self.env.context.get('noset_use', False):
            self.use = 'some_values'
