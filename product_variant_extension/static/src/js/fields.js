odoo.define('product_variant_extension.boolean', function(require){
    "use strict"
    var AbstractField =require('web.AbstractField');
    var fieldRegistry = require('web.field_registry')
    var boolean_button =AbstractField .extend({
    className:'o_field_boolean_button',
    events: {
        'click': '_setaddorremove'
    },
    supportedFieldTypes: ['boolean'],

    isSet: function () {
        return true;
    },
    _render:function(){
        var template = '<div>%s<a href="#"/></div>';
        this.$el.empty().append(_.str.sprintf(template, 'Add/Remove'));
    },
    _setaddorremove: function (event) {
        event.preventDefault();
        event.stopPropagation();
        if (this.mode === 'readonly') {
            return this.trigger_up('bounce_edit');
        }
        this._setValue(!this.value);
    },
    });
    fieldRegistry.add('cboolean_button',boolean_button);
});