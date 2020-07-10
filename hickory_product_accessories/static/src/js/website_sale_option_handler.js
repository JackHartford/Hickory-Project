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
             var refreshId = setInterval(function(){
                if($(".oe_optional_products_modal").length > 0){
                    let mandatory_prod_ids = $("input[name='mandatory_mapping']").val()
                     if (mandatory_prod_ids){
                        mandatory_prod_ids = JSON.parse(mandatory_prod_ids);
                        if (mandatory_prod_ids && mandatory_prod_ids.length >0){
                            $.each(mandatory_prod_ids , function(i, item) {
                                 let ele = $(".oe_optional_products_modal .js_product div[data-oe-model='product.template'][data-oe-id='" + item +"']").closest('.td-product_name')
                                 $(ele).find('.float-left').prepend('<img class="mandatory_icon" src="/hickory_product_accessories/static/description/mandatory_icon.png" />')
                            });
                        }
                     }
                     clearInterval(refreshId);
                }
             }, 100);
        },
         _onOptionsUpdateQuantity: function (quantity) {
             this._super.apply(this, arguments);
             $(".oe_optional_products_modal .js_product.in_cart").find(".mandatory_icon").remove();
             $(".oe_optional_products_modal .js_product.in_cart").find(".mandatory-required").remove();
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
                ev.preventDefault();
            }else{
                this._super.apply(this, arguments);
            }
        },
    });
})