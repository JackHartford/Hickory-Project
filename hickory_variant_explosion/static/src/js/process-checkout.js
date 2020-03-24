odoo.define('hickory_variant_explosion.process-checkout', function (require) {
    "use strict";
    var OptionalProductsModal = require('sale.OptionalProductsModal');
    /*var weContext = require('web_editor.context');
    var sAnimations = require('website.content.snippets.animation');
    sAnimations.registry.WebsiteSaleOptions.include({
    	_onModalSubmit: function (goToShop){
    		var optional_values = this.optionalProductsModal.getSelectedProducts();
    		var mandatory_values = this.optionalProductsModal.getSelectedMandatoryProduct();
    		// console.log("optional_values", optional_values);
    		// console.log("mandatory_values", mandatory_values);
    		var values = $.merge(optional_values, mandatory_values);
    		// console.log("values", values);
    		var customValues = JSON.stringify(
				values
			);
			// console.log("customValues", customValues);
			this.$form.ajaxSubmit({
				url: '/shop/cart/update_option',
				data: {		
					lang: weContext.get().lang,
					custom_values: customValues
				},
				success: function (quantity) {
					if (goToShop) {
						var path = window.location.pathname.replace(/shop([\/?].*)?$/, "shop/cart");
						window.location.pathname = path;
					}
					var $quantity = $(".my_cart_quantity");
					$quantity.parent().parent().removeClass("d-none", !quantity);
					$quantity.html(quantity).hide().fadeIn(600);
				}
			});
		},
    })*/
    OptionalProductsModal.include({
    	events: _.extend({}, OptionalProductsModal.prototype.events, {
    		'click .mandatory_options_add': '_onClickButtonProcessAdd',
    		//'click .mandatory_options_remove': '_onClickButtonProcessRemove'
    	}),
    	init: function (parent, params) {
	        var self = this;

	        var options = _.extend({
	            size: 'large',
	            buttons: [{
	                text: params.okButtonText,
	                click: this._onConfirmButtonClick,
	                classes: 'btn-primary continue-process',
	                disabled: true
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
    	//_onClickButtonProcessAdd: function(ev){
	        //var $target = $(ev.currentTarget);
	        /*var clicked_product = _.find($('.js_add'), function(click){
	            return $(click).click(function(){
	            	console.log(clicked_product);
		            if($(clicked_product).length){
			            $('.continue-process').prop('disabled',false);
			        }
			        else{
			            $('.continue-process').prop('disabled',true);
			        }
			    });    
	        });*/
	        //$('.continue-process').prop('disabled',false);
	        /*var $parent = $target.parents('.js_product:first');
	        console.log("$parent", $parent)
	        console.log("xxxxxxxxx", $parent.find("input.js_mandatory_same_quantity"));
	        $parent.find("input.js_mandatory_same_quantity").val($(checked_product).length ? 1 : 0);*/
	    //},
	    /*_onClickButtonProcessRemove: function(ev){

	    	$('.continue-process').prop('disabled',true);
	    	console.log("Testing click");*/
	    /*getSelectedMandatoryProduct: function(){
	    	var products = [];
	    	var selectedProduct = _.filter($('.checkout-process'), function(checkbox){
	            return $(checkbox).prop("checked");
	        });
	        // console.log("selectedProduct", selectedProduct);
	        _.each(selectedProduct, function(product){
	        	products.push({
	        		product_id: parseInt($(product).data('product')),
	        		quantity: 1,
	        		product_custom_attribute_values: [],
                	no_variant_attribute_values: [],
	        	})

	        });
		    return products;
	    },*/
	   // },	
	    _onAddOrRemoveOption: function (ev){
	    	this._super.apply(this, arguments);
	    	var $target = $(ev.currentTarget);
	    	if ($target.hasClass('mandatory_options_add')) {
            	$('.continue-process').prop('disabled',false);
	        } else {
	        	var temp_remove_product = _.find($('tr.in_cart'), function(row){
	        		return $(row).hasClass('mandatory_product');
	        	})
	        	if(!temp_remove_product){
	            	$('.continue-process').prop('disabled',true)
	        	}
	        }
	    },
    });
}
);
