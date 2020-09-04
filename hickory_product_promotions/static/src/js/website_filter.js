odoo.define('hickory_product_promotions.website_sale', function (require) {
    "use strict";

    require('web.dom_ready');

    $('.oe_website_sale').each(function (el) {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', 'select.js_variant_change', function (event) {

            var $parent = $(this).closest('.js_product');
            var attribute_value_ids = $(this).closest('.js_add_cart_variants').data("attribute_value_ids");

            if(_.isString(attribute_value_ids)) {
                attribute_value_ids = JSON.parse(attribute_value_ids.replace(/'/g, '"'));
            }

            var variant_ids = _(attribute_value_ids).map(function(val){
                return _.sortBy(val[1]);
            });

            var values = [];
            $parent.find("select.js_variant_change").each(function () {
                values.push(+$(this).val());
            });

            $parent.find("select.js_variant_change").each(function () {
                var selection = this;
                var value = +selection.value;
                var comp_values = _.without(values, value);
                $(this).find('option').not("option[value='" + value + "']").each(function(){
                    var vals = comp_values.concat([+this.value]);
                    var product = _(variant_ids).filter(function(variant){ return !_.difference(vals, variant).length; });

                    if (product.length) {
//                        $(this).css('display', 'block');
                        $(this).removeClass('css_not_available');

                    } else {
//                        $(this).css('display', 'block');
                    }
                });
            });
        });

        if ($('div.css_not_available.js_product ').length) {
            var attribute_value_ids = $(this).find('.js_add_cart_variants:first').data("attribute_value_ids");

            if(_.isString(attribute_value_ids)) {
                attribute_value_ids = JSON.parse(attribute_value_ids.replace(/'/g, '"'));
            }

            var variant_id = attribute_value_ids[0][1];

            $(this).find("select.js_variant_change option").each(function () {
                if (variant_id.indexOf(+this.value) != -1) {
                    this.selected = true;
                    $(this).removeClass('css_not_available');
                }
            });
        }
        $('select.js_variant_change').trigger('change');
    });

});
