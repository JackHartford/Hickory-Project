# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def setup_defaults(self):
        """
        Configure default settings for the Inventory module. This function will be
        used during update and install of the hickory_variant_explosion module so that
        we can include all the settings that this module needs to operate.

        :return: None
        """
        update_vals = {}

        # Get all of the fields and their values
        config_vals = self.env['res.config.settings'].default_get(self.env['res.config.settings']._get_classified_fields())
        # Now get each setting so we can check it's value
        variants_enabled = config_vals.get('group_product_variant', False)

        # Check each setting's value to be sure it's what we want it to be
        if not variants_enabled:
            update_vals['group_product_variant'] = True
        
        # Create and update new temporary record so we can change these settings
        # If there's nothing to do, don't waste anymore resources
        if update_vals:
            config_id = self.env['res.config.settings'].create({})
            config_id.update(update_vals)
            config_id.execute()
