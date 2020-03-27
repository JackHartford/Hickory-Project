# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import itertools
import copy

class ExistProductVariants(models.TransientModel):
    _name = "exist.product.variants"

    default_code = fields.Char('Internal Reference', index=True)
    attribute_value_ids = fields.Many2many('product.attribute.value', string='Attribute Values')
    variant_create_id = fields.Many2one('product.variant.create', string="Existing Variants")


class NewProductVariants(models.TransientModel):
    _name = "new.product.variants"

    default_code = fields.Char('Internal Reference', index=True)
    sq_no = fields.Integer('Sequence')
    attribute_value_ids = fields.Many2many('product.attribute.value', string='Attribute Values')
    new_variant_id = fields.Many2one('product.variant.create', string="New Variants to Create")
    add_flag = fields.Boolean("Add", default=True)


class ProductVariantCreate(models.TransientModel):
    _name = "product.variant.create"

    product_id = fields.Many2one('product.template', string="Master Product")
    exist_variant_ids = fields.One2many('exist.product.variants', 'variant_create_id', string="Existing Variants")
    new_variant_ids = fields.One2many('new.product.variants', 'new_variant_id', string="New Variants to Create")

    @api.model
    def default_get(self, fields):
        result = super(ProductVariantCreate, self).default_get(fields)
        product_template = self.env['product.template']
        product_template_ids = product_template.browse(self._context.get('active_ids'))
        exist_vals = []
        exist_attrib_list =[]
        for template in product_template_ids:
            for variant in template.product_variant_ids:
                exist_attrib_list.append(sorted(variant.attribute_value_ids.ids))
                exist_vals.append(
                    (0, 0, {'default_code': variant.default_code,
                            'attribute_value_ids': variant.attribute_value_ids.ids}))
            variants_to_create = []
            print('exist_attrib_list-----------------',exist_attrib_list)


            if not template.has_dynamic_attributes():
                # Iterator containing all possible `product.attribute.value` combination
                # The iterator is used to avoid MemoryError in case of a huge number of combination.
                all_variants = itertools.product(*(
                    line.value_ids.ids for line in template.valid_product_template_attribute_line_wnva_ids
                    # line.value_ids.ids for line in template.valid_product_template_attribute_line_wnva_ids.filtered(lambda val: not val.explode_flag)
                ))
                print('all_variants', all_variants)
                print('template.valid_product_template_attribute_line_wnva_ids', template.valid_product_template_attribute_line_wnva_ids)
                # Set containing existing `product.attribute.value` combination
                existing_variants = {
                    frozenset(variant.attribute_value_ids.ids)
                    for variant in template.product_variant_ids
                }
                print('existing_variants', existing_variants)
                # For each possible variant, create if it doesn't exist yet.
                sq_no = 1

                allowed_combination = []
                for line in template.attribute_condition_ids:
                    final_value_list = line.attribute_value_ids.ids
                    final_value_list.append(line.value_id.id)
                    allowed_combination.append(final_value_list)
                allowed_combination = [i for n, i in enumerate(allowed_combination) if i not in allowed_combination[:n]]

                print('allowed_combination444444444444', allowed_combination)

                # for comb in allowed_combination:
                #     for line in template.attribute_condition_ids:
                #         if set(line.attribute_value_ids.ids).issubset(set(comb)):
                #             comb.append(line.value_id.id)
                # print('allowed_combination', allowed_combination)
                # allwd_dict = {}
                # allowed_val = copy.copy(allowed_combination)
                # product_att_val = self.env['product.attribute.value']
                # for comb in allowed_val:
                #     attribute_id = product_att_val.browse(comb[0]).attribute_id
                #     if attribute_id.id in allwd_dict:
                #         print('----------',allwd_dict)
                #         allwd_dict[attribute_id.id].append(comb)
                #     else:
                #         allwd_dict[attribute_id.id] = [comb]

                final_variants = copy.copy(all_variants)

                if any(not val.explode_flag for val in template.attribute_line_ids) and any(val.explode_flag for val in template.attribute_line_ids):
                    filtered_all_variants = []
                    for value_ids in all_variants:
                        for existing_variant in existing_variants:
                            if set(value_ids).issuperset(set(existing_variant)):
                                filtered_all_variants.append(value_ids)
                    filtered_all_variants = list(set(filtered_all_variants))
                    print('filtered_all_variants', filtered_all_variants)
                    print('filtered_all_variants------------', len(filtered_all_variants))
                    final_variants = filtered_all_variants

                for value_ids in final_variants:
                    # print('value_ids', value_ids)
                    value_ids = frozenset(value_ids)
                    value_ids_list = sorted(list(value_ids))
                    # print('value_ids_list', value_ids_list)

                    if value_ids and value_ids not in existing_variants and not template.attribute_condition_ids:
                        variants_to_create.append((0, 0, {
                            'sq_no': sq_no,
                            'add_flag': True,
                            'attribute_value_ids': list(value_ids),
                        }))
                        sq_no += 1

                    if value_ids and value_ids not in existing_variants and template.attribute_condition_ids.ids:
                        chk_flg =[]
                        for allowed_comb in allowed_combination:
                            print('value_ids_list', value_ids_list)
                            print('allowed_comb', allowed_comb)
                            if set(allowed_comb).issubset(set(value_ids_list)):
                                chk_flg.append(True)
                            else:
                                chk_flg.append(False)
                        if True in chk_flg:
                            variants_to_create.append((0, 0, {
                                'sq_no': sq_no,
                                'add_flag': True,
                                'attribute_value_ids': list(value_ids),
                            }))
                            sq_no += 1

            # explode_variants_to_create = variants_to_create
            # newly_creating_explode = 0
            # if not variants_to_create:
            #     variants_to_create = template.product_variant_ids
            #     newly_creating_explode = 1
            #
            # print('variants_to_create',variants_to_create)
            # if any(val.explode_flag for val in template.attribute_line_ids):
            #     print('inside----------------------------->')
            #     sq_no = 1
            #     length_new_variant = len(variants_to_create)
            #     print('length_new_variant',length_new_variant)
            #     explode_variants_to_create = []
            #
            #     for res in template.attribute_line_ids.filtered(lambda val: val.explode_flag):
            #         if explode_variants_to_create == []:
            #             dup_count = length_new_variant
            #             print('dup_count', dup_count)
            #             value_count = len(res.value_ids)
            #             print('value_count', value_count)
            #
            #             if dup_count > 0 and value_count > 0:
            #                 value_ids = res.value_ids.ids
            #                 print('value_ids', value_ids)
            #                 for count in range(value_count):
            #                     for each in variants_to_create:
            #                         if newly_creating_explode == 0:
            #                             exist_att = each[2]['attribute_value_ids'][:]
            #                         else:
            #                             exist_att = each.attribute_value_ids.ids[:]
            #                         exist_att.append(value_ids[count])
            #                         if sorted(exist_att) not in exist_attrib_list:
            #                             explode_variants_to_create.append((0, 0, {
            #                                 'sq_no': sq_no,
            #                                 'add_flag': True,
            #                                 'attribute_value_ids': exist_att,
            #                             }))
            #                             sq_no += 1
            #         else:
            #             print('explode_variants_to_create-------------',explode_variants_to_create)
            #             dup_count = len(explode_variants_to_create)
            #             print('dup_count', dup_count)
            #             value_count = len(res.value_ids)
            #             print('value_count', value_count)
            #             variants_to_create = explode_variants_to_create[:]
            #             explode_variants_to_create.clear()
            #             newly_creating_explode = 0
            #             sq_no = 1
            #             if dup_count > 0 and value_count > 0:
            #                 value_ids = res.value_ids.ids
            #                 print('value_ids', value_ids)
            #                 for count in range(value_count):
            #                     for each in variants_to_create:
            #                         if newly_creating_explode == 0:
            #                             exist_att = each[2]['attribute_value_ids'][:]
            #                         else:
            #                             exist_att = each.attribute_value_ids.ids[:]
            #                         exist_att.append(value_ids[count])
            #                         if sorted(exist_att) not in exist_attrib_list:
            #                             explode_variants_to_create.append((0, 0, {
            #                                 'sq_no': sq_no,
            #                                 'add_flag': True,
            #                                 'attribute_value_ids': exist_att,
            #                             }))
            #                             sq_no += 1



        result['exist_variant_ids'] = exist_vals
        result['new_variant_ids'] = variants_to_create
        result['product_id'] = self._context.get('active_id', False)
        return result

    # @api.multi
    # def create_product(self):
    #     self.ensure_one()
    #     Product = self.env["product.product"]
    #     product_template = self.env['product.template']
    #     product_template_ids = product_template.browse(self._context.get('active_ids'))
    #     to_create_variants = self.new_variant_ids.filtered(lambda line: line.add_flag)
    #     for tmpl_id in product_template_ids:
    #         variants_to_create = []
    #         for each in to_create_variants:
    #             variants_to_create.append({
    #                 'product_tmpl_id': tmpl_id.id,
    #                 'attribute_value_ids': [(6, 0, each.attribute_value_ids.ids)],
    #                 'active': tmpl_id.active,
    #             })
    #         if variants_to_create:
    #             for res in tmpl_id.attribute_line_ids:
    #                 res.processed = True
    #             for res in tmpl_id.attribute_condition_ids:
    #                 res.flg = True
    #             for variant in tmpl_id.product_variant_ids:
    #                 try:
    #                     with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
    #                         variant.unlink()
    #                 except:
    #                     print('variant', variant)
    #                     variant.write({'active': False})
    #             product_id = Product.create(variants_to_create)
    #     return True

    @api.multi
    def create_product(self):
        self.ensure_one()
        Product = self.env["product.product"]
        product_template = self.env['product.template']
        product_template_ids = product_template.browse(self._context.get('active_ids'))
        for tmpl_id in product_template_ids:
            # Handle the variants for each template separately. This will be
            # less efficient when called on a lot of products with few variants
            # but it is better when there's a lot of variants on one template.
            variants_to_create = []
            variants_to_activate = self.env['product.product']
            variants_to_unlink = self.env['product.product']
            # adding an attribute with only one value should not recreate product
            # write this attribute on every product to make sure we don't lose them

            to_create_variants = self.new_variant_ids.filtered(lambda line: line.add_flag)
            to_create_variants_list = []
            for each in to_create_variants:
                to_create_variants_list.append(frozenset(each.attribute_value_ids.ids))

            # Determine which product variants need to be created based on the attribute
            # configuration. If any attribute is set to generate variants dynamically, skip the
            # process.
            # Technical note: if there is no attribute, a variant is still created because
            # 'not any([])' and 'set([]) not in set([])' are True.
            if not tmpl_id.has_dynamic_attributes():
                # Iterator containing all possible `product.attribute.value` combination
                # The iterator is used to avoid MemoryError in case of a huge number of combination.
                all_variants = itertools.product(*(
                    line.value_ids.ids for line in tmpl_id.valid_product_template_attribute_line_wnva_ids
                ))
                # Set containing existing `product.attribute.value` combination
                existing_variants = {
                    frozenset(variant.attribute_value_ids.ids)
                    for variant in tmpl_id.product_variant_ids
                }
                # For each possible variant, create if it doesn't exist yet.

                allowed_combination = []
                for line in tmpl_id.attribute_condition_ids:
                    final_value_list = line.attribute_value_ids.ids
                    final_value_list.append(line.value_id.id)
                    allowed_combination.append(final_value_list)
                allowed_combination = [i for n, i in enumerate(allowed_combination) if i not in allowed_combination[:n]]

                # for comb in allowed_combination:
                #     for line in tmpl_id.attribute_condition_ids:
                #         if set(line.attribute_value_ids.ids).issubset(set(comb)):
                #             comb.append(line.value_id.id)
                #
                # allwd_dict = {}
                # allowed_val = copy.copy(allowed_combination)
                # product_att_val = self.env['product.attribute.value']
                # for comb in allowed_val:
                #     attribute_id = product_att_val.browse(comb[0]).attribute_id
                #     if attribute_id.id in allwd_dict:
                #         print('----------', allwd_dict)
                #         allwd_dict[attribute_id.id].append(comb)
                #     else:
                #         allwd_dict[attribute_id.id] = [comb]

                final_variants = copy.copy(all_variants)

                if any(not val.explode_flag for val in tmpl_id.attribute_line_ids) and any(
                        val.explode_flag for val in tmpl_id.attribute_line_ids):
                    filtered_all_variants = []
                    for value_ids in all_variants:
                        for existing_variant in existing_variants:
                            if set(value_ids).issuperset(set(existing_variant)):
                                filtered_all_variants.append(value_ids)
                    filtered_all_variants = list(set(filtered_all_variants))
                    print('filtered_all_variants', filtered_all_variants)
                    final_variants = filtered_all_variants

                for att_line in tmpl_id.attribute_line_ids:
                    att_line.explode_flag = True

                # for value_ids in filtered_all_variants:
                for value_ids in final_variants:
                    print('value_ids', value_ids)
                    value_ids = frozenset(value_ids)
                    value_ids_list = list(value_ids)

                    if value_ids and value_ids not in existing_variants and not tmpl_id.attribute_condition_ids and value_ids in to_create_variants_list:
                        variants_to_create.append({
                            'product_tmpl_id': tmpl_id.id,
                            'attribute_value_ids': [(6, 0, list(value_ids))],
                            'active': tmpl_id.active,
                        })

                    if value_ids and value_ids not in existing_variants and tmpl_id.attribute_condition_ids.ids:
                        chk_flg = []
                        for allowed_comb in allowed_combination:
                            print('value_ids_list', value_ids_list)
                            print('allowed_comb', allowed_comb)
                            if set(allowed_comb).issubset(set(value_ids_list)):
                                chk_flg.append(True)
                            else:
                                chk_flg.append(False)
                        if True in chk_flg:
                                variants_to_create.append({
                                    'product_tmpl_id': tmpl_id.id,
                                    'attribute_value_ids': [(6, 0, list(value_ids))],
                                    'active': tmpl_id.active,
                                })


            valid_value_ids = tmpl_id.valid_product_attribute_value_wnva_ids
            valid_attribute_ids = tmpl_id.valid_product_attribute_wnva_ids
            seen_attributes = set(p.attribute_value_ids for p in tmpl_id.product_variant_ids if p.active)
            for product_id in tmpl_id.product_variant_ids:
                if product_id._has_valid_attributes(valid_attribute_ids, valid_value_ids):
                    if not product_id.active and product_id.attribute_value_ids not in seen_attributes:
                        variants_to_activate += product_id
                        seen_attributes.add(product_id.attribute_value_ids)
                else:
                    variants_to_unlink += product_id

            if variants_to_activate:
                variants_to_activate.write({'active': True})

            # create new products
            if variants_to_create:
                product_id = Product.create(variants_to_create)
                print('Product_id', product_id)

            # Avoid access errors in case the products is shared amongst companies but the underlying
            # objects are not. If unlink fails because of an AccessError (e.g. while recomputing
            # fields), the 'write' call will fail as well for the same reason since the field has
            # been set to recompute.
            if variants_to_unlink:
                variants_to_unlink.check_access_rights('unlink')
                variants_to_unlink.check_access_rule('unlink')
                variants_to_unlink.check_access_rights('write')
                variants_to_unlink.check_access_rule('write')
                variants_to_unlink = variants_to_unlink.sudo()
            # unlink or inactive product
            # try in batch first because it is much faster
            try:
                with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                    variants_to_unlink.unlink()
            except Exception:
                # fall back to one by one if batch is not possible
                for variant in variants_to_unlink:
                    try:
                        with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                            variant.unlink()
                    # We catch all kind of exception to be sure that the operation doesn't fail.
                    except Exception:
                        # Note: this can still fail if something is preventing from archiving.
                        # This is the case from existing stock reordering rules.
                        variant.write({'active': False})
        # prefetched o2m have to be reloaded (because of active_test)
        # (eg. product.template: product_variant_ids)
        # We can't rely on existing invalidate_cache because of the savepoint.
        self.invalidate_cache()
        return True
