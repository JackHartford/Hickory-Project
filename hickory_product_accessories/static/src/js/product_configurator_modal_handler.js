odoo.define('hickory_product_accessories.product_configurator_modal_handler', function (require) {
'use strict';

var core = require('web.core');
var ProductConfiguratorModalHandler = require('sale.OptionalProductsModal');
var _t = core._t;
    ProductConfiguratorModalHandler.include({
        init: function () {
            this._super.apply(this, arguments);
        },
         _onCancelButtonClick: function () {
            this.trigger('back');
//            if(isClose == undefined){
//              this.close();
//            }
        },
    });
})