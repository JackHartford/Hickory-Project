odoo.define('hickory_product_accessories.product_configurator_modal_handler', function (require) {
'use strict';

var core = require('web.core');
var ProductConfiguratorModalHandler = require('sale.OptionalProductsModal');
var _t = core._t;
    ProductConfiguratorModalHandler.include({
        init: function (parent, params) {
            var self = this;

            var options = _.extend({
                size: 'large',
                buttons: [{
                    text: params.okButtonText,
                    click: this._onConfirmButtonClick,
                    classes: 'btn-primary'
                }, {
                    text: params.cancelButtonText,
                    click: this._onCancelButtonClick
                }],
                technical: !params.isWebsite,
            }, params || {});

            this._super(parent, options);

            this.rootProduct = params.rootProduct;
            this.container = parent;
            this.pricelistId = params.pricelistId;
            this.isWebsite = params.isWebsite;
            this.dialogClass = 'oe_optional_products_modal' + (params.isWebsite ? ' oe_website_sale' : '');
            this._productImageField = 'image_medium';
        },
         _onCancelButtonClick: function () {
            this.trigger('back');
//            if(isClose == undefined){
//              this.close();
//            }
        },
        start: function () {
            var def = this._super.apply(this, arguments);
            var self = this;

            this.$el.find('input[name="add_qty"]').val(this.rootProduct.quantity);

            return def.then(function () {
                // This has to be triggered to compute the "out of stock" feature
                self._opened.then(function () {
                    self.triggerVariantChange(self.$el);
                });
            });
        },
        _onAddOrRemoveOption: function (ev){
	    	this._super.apply(this, arguments);
	    },
    });
})