odoo.define('hickory.product_attribute', function (require) {
    "use strict";
    require('web.dom_ready');
    var attrs = JSON.parse($("input[name='prod_variants']").val().replace(/'/g, '"'))
    $('.oe_website_sale').each(function (el) {
        var oe_website_sale = this;
        // filter attribute on load
        filterAttributes(oe_website_sale);
        // auto fill on change
        $(oe_website_sale).on('change', 'select.js_variant_change', function (event) {
            var $parent = $(this).closest('.js_product');
            $parent.find("select.js_variant_change").each(function () {
                 //  auto filter attributes first
                 filterAttributes(oe_website_sale);
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
        });
    });

//  auto filter attributes base on allow attributes values
    function autoMatchAttributes(params){
        if(params && params['key'] !== undefined && params['value'] !== undefined){
            let key = params['key']
            let value = params['value']
            let selection = params['selection']
            $.each(attrs, function(i, item) {
                if(item.hasOwnProperty(key) && item[key] == value){
                    //  match with correct attributes
                    let variant_attrs = $('.oe_website_sale').find('.list-inline-item.variant_attribute');
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
        }
    }

//  filter attributes base on allow attributes values
    function filterAttributes(element){
       var oe_website_sale = element;
        $(oe_website_sale).find('select.js_variant_change').each(function () {
            let ele = this;
            let key = $(ele).closest('.list-inline-item.variant_attribute').attr('data-attribute_name')
            let options = $(ele).find("option")
            $.each(options, function(i, op) {
                let isMatch = false;
                $.each(attrs, function(j, item) {
                    if (!item.hasOwnProperty(key) || (item.hasOwnProperty(key) && $(op).attr("data-value_name") == item[key])){
                        isMatch = true;
                   }
                });
                if (!isMatch){
                    $(op).hide();
                }
            });

        });
    }

});

