odoo.define('hickory.product_attribute', function (require) {
    "use strict";
    require('web.dom_ready');
    console.log($("input[name='prod_variants']").val())
    attrs = JSON.parse($("input[name='prod_variants']").val().replace(/'/g, '"'))
    $('.oe_website_sale').each(function (el) {
        var oe_website_sale = this;

        $(oe_website_sale).on('change', 'select.js_variant_change', function (event) {

            var $parent = $(this).closest('.js_product');

            $parent.find("select.js_variant_change").each(function () {
                 attr_name = $(selection).prev('.attribute_name').html()
                 attr_val = $(selection).find("option[selected='True']").attr("data-value_name")

            });
        });
    });

    function getMatchAttr(params){
        if(params && params['key'] !== undefined && params['value'] !== undefined){
            let key = params['key']
            let value = params['value']
            let matches = []
            $.each(attrs, function(i, item) {
                if(key in i && value in attrs[i]){
                    matches.push(attrs[i])
                }
            });
        }
    }

});

