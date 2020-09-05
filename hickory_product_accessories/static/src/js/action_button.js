
odoo.define('hickory_product_accessories.action_button', function (require) {
"use strict";
var core = require('web.core');
var BasicController = require('web.BasicController');
var DataExport = require('web.DataExport');
var ListController = require('web.ListController');
    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
                let action_button = this.$buttons.find('.oe_action_button');
                action_button && action_button.click(this.proxy('action_button'));
                let action_att_button = this.$buttons.find('.oe_action_button_att_value');
                action_att_button && action_att_button.click(this.proxy('action_att_button'));
            }
        },
        action_button: function () {
            var self = this;
            this._rpc({
                model: 'product.product',
                method: 'cal_priority'
            }).then(function (result) {
                if (result) {
                     self.trigger_up('reload');
                }
            });
        },
        action_att_button: function () {
            var self = this;
            this._rpc({
                model: 'product.attribute.value',
                method: 'cal_priority'
            }).then(function (result) {
                if (result) {
                     self.trigger_up('reload');
                }
            });
        },
        init: function() {
            var self = this;
            this._super.apply(this, arguments);
        },
    });
})