odoo.define('hickory_product_accessories.website_sale_option_handler', function (require) {
'use strict';

var core = require('web.core');
var WebsiteSaleOptions = require('website_sale_options.website_sale');
var _t = core._t;
    WebsiteSaleOptions.include({
        init: function () {
            this._super.apply(this, arguments);
        },
        _handleAdd: function (ev) {
            this._super.apply(this, arguments)
            self = this;
            let count = 0;
             var refreshId = setInterval(function(){
                if(count > 10){
                     clearInterval(refreshId);
                }
                count+=1;
                if($(".oe_optional_products_modal").length > 0){
                    $('.continue-process').prop('disabled',false)
                    let mandatory_prod_ids = $("input[name='mandatory_mapping']").val()
                     if (mandatory_prod_ids){
                        mandatory_prod_ids = JSON.parse(mandatory_prod_ids);
                        if (mandatory_prod_ids && mandatory_prod_ids.length >0){
                            $.each(mandatory_prod_ids , function(i, item) {
                                 let ele = $(".oe_optional_products_modal .js_product input[class='product_template_id'][value='" + item +"']").closest('.td-img').next('.td-product_name')
                                 $(ele).find('.float-left').prepend('<img class="mandatory_icon" src="/hickory_product_accessories/static/description/mandatory_icon.png" />')
                                  $('.continue-process').prop('disabled',true)
                            });
                        }
                     }
                     var $op_products = $(".oe_optional_products_modal .js_product:not(.in_cart)");

                     $op_products.find("select.js_variant_change").each(function () {
                         //  auto filter attributes first
                         self._filterAttributes($op_products);
                     });
                     $op_products.each(function () {
                         $(this).find(".td-product_name .product-name").after('<div class="btn mt8 js_reset_variant" >Reset</div>')
                     });
                     clearInterval(refreshId);
                }
             }, 100);
        },
         _onOptionsUpdateQuantity: function (quantity) {
             this._super.apply(this, arguments);
             $(".oe_optional_products_modal .js_product.in_cart").find(".mandatory_icon").remove();
             $(".oe_optional_products_modal .js_product.in_cart").find(".mandatory-required").remove();
             if($(".oe_optional_products_modal .js_product:not(.in_cart)").find(".mandatory_icon").length > 0){
                $('.continue-process').prop('disabled',true)
             }else{
                $('.continue-process').prop('disabled',false)
             }
        },
        _onModalBack: function (ev) {
            let cart = $(".oe_optional_products_modal .js_product:not(.in_cart)");
            if($(cart).find("img[class='mandatory_icon']").length > 0){
                let p_eles = $(cart).find("img[class='mandatory_icon']")
                $.each($(p_eles) , function(i, item) {
                    if ($(item).closest(".td-product_name").find(".mandatory-required").length == 0){
                        $("<p class='mandatory-required'>You must add this item to the cart to continue the checkout process</p>").insertAfter($(item).closest(".td-product_name").find(".product-name"))
                    }
                });
            }else{
                this._super.apply(this, arguments);
                $(".oe_optional_products_modal").closest(".modal ").modal('hide')
            }
        },
        _filterAttributes: function (element) {
           var oe_website_sale = element;
            if ($(element).closest('.oe_optional_products_modal').length > 0){
                oe_website_sale = $(element).closest('.oe_optional_products_modal')
            }
            $(oe_website_sale).find('select.js_variant_change').each(function () {
                let ele = this;
                let key = $(ele).closest('.list-inline-item.variant_attribute').attr('data-attribute_name')
                let options = $(ele).find("option")
                $.each(options, function(i, op) {
                    let isMatch = false;
                    var parent = $(this).closest('.js_product');
                    var product_id = $(parent).find("input[class='product_template_id']").val()
                    var a_attrs = JSON.parse($("input[name='prod_variants']").val())
                    var p_attrs = a_attrs[product_id]
                    $.each(p_attrs, function(j, item) {
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
})