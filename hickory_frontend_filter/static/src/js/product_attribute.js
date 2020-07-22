odoo.define('hickory.product_attribute', function (require) {
    "use strict";
    require('web.dom_ready');
    var attrs = JSON.parse($("input[name='prod_variants']").val().replace(/'/g, '"'))
    var isFinishFilter = false;
    $('.oe_website_sale').each(function (el) {
        var oe_website_sale = this;
        // filter attribute on load
        filterAttributes(oe_website_sale);
        // auto fill on change
        $(document).on('change', 'select.js_variant_change', function (event) {
//            if ($(this).closest('.oe_optional_products_modal').length <= 0){
                var $parent = $(this).closest('.js_product');

                $parent.find("select.js_variant_change").each(function () {
                     //  auto filter attributes first
                     filterAttributes($parent);
                });
                let selection = this;
                 let attr_name = $(selection).prev('.attribute_name').html()
                 let val = $(selection).val()
                 let attr_val = $(selection).find("option[value='"+ val +"']").attr("data-value_name")
                 //  auto match attributes
                 autoMatchAttributes({
                    'key': attr_name,
                    'value': attr_val,
                    'selection': selection
                 })
//            }
        });
    });

//  auto filter attributes base on allow attributes values
    function autoMatchAttributes(params){
        if(params && params['key'] !== undefined && params['value'] !== undefined){
            let key = params['key']
            let value = params['value']
            let selection = params['selection']
            var parent = $(selection).closest('.js_product');
            var product_id = $(parent).find("input[class='product_template_id']").val()
            var p_attrs = attrs[product_id]
            $.each(p_attrs, function(i, item) {
                if(item.hasOwnProperty(key) && item[key] == value){
                    //  match with correct attributes
                    let variant_attrs = $(parent).find('.list-inline-item.variant_attribute');
                    $.each(item, function(j, otVal) {
                         if($(variant_attrs).find("select").length > 0){
                             let corOption = $(variant_attrs).find("option[data-attribute_name='" + j +"'][data-value_name='" + otVal +"']");
                             let sel = $(corOption).closest('select');
                             let val = $(corOption).val();
                             if($(sel)[0] != $(selection)[0]){
                                $(sel).val(val);
                             }
                         }
                    });
                    return false;
                }
            });
            window.isFinishFilter = true;
        }
    }

//  filter attributes base on allow attributes values
    function filterAttributes(element){
       var oe_website_sale = element;
        if ($(element).closest('.oe_optional_products_modal').length > 0){
            oe_website_sale = $(element).closest('.oe_optional_products_modal')
        }
        $(oe_website_sale).find('select.js_variant_change').each(function () {
//            if ($(this).closest('.oe_optional_products_modal').length <= 0){
                let ele = this;
                let key = $(ele).closest('.list-inline-item.variant_attribute').attr('data-attribute_name')
                let options = $(ele).find("option")
                $.each(options, function(i, op) {
                    let isMatch = false;
                    var parent = $(this).closest('.js_product');
                    var product_id = $(parent).find("input[class='product_template_id']").val()
                    var p_attrs = attrs[product_id]
                    $.each(p_attrs, function(j, item) {
                        if (!item.hasOwnProperty(key) || (item.hasOwnProperty(key) && $(op).attr("data-value_name") == item[key])){
                            isMatch = true;
                       }
                    });
                    if (!isMatch){
                        $(op).hide();
                    }
                });
//            }

        });
    }

});

