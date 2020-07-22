odoo.define('hickory_product_accessories.product_accessory', function (require) {
'use strict';

var core = require('web.core');
var weContext = require('web_editor.context');
var sAnimations = require('website.content.snippets.animation');
var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
var ajax = require('web.ajax');

sAnimations.registry.Product_Accessory = sAnimations.Class.extend(ProductConfiguratorMixin, {
   selector: '.oe_website_sale',
    read_events: {
        'change .js_main_product [data-attribute_exclusions]': 'onChangeCustomVariant',
    },

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
    },
    onChangeCustomVariant: function (ev) {
        let count = 0;
        var self = this;
        var refreshId = setInterval(function(){
                if(count > 10){
                     clearInterval(refreshId);
                     window.isFinishFilter = false;
                }
                count+=1;
                if(window.isFinishFilter){
                     clearInterval(refreshId);
                     window.isFinishFilter = false;
                     if(ev.originalEvent != undefined){
                        let arr = []
                        $('.oe_website_sale .js_product.js_main_product select.js_variant_change').each(function () {
                            let ele = this;
                            let val = $(ele).val();
                            let attr_name = $(ele).find("option[value='" + val + "']").attr("data-attribute_name")
                            let value_name = $(ele).find("option[value='" + val + "']").attr("data-value_name")
                            arr.push({
                                'attr': attr_name,
                                'value': value_name
                            })
                        });
                        var $parent = $(ev.target).closest('.js_product');
                        var productTemplateId = parseInt($parent.find('.product_template_id').val());
                        $("#add_to_cart").bind('click', function(e){
                                e.preventDefault();
                        })
                        return ajax.jsonRpc(self._getUri('/product_configurator/set_optional_product_accessory'), 'call', {
                            'attrs': JSON.stringify(arr),
                            'product_template_id': productTemplateId,
                        }).then(function (res) {
                            if(res){
                                $("input[name='mandatory_mapping']").val(JSON.stringify(res))
                                $("#add_to_cart").unbind('click')
                            }
                        });
                    }
                }
        }, 100);
    },
});

return sAnimations.registry.Product_Accessory;

});
