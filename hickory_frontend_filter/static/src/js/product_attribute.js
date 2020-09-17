odoo.define('hickory.product_attribute', function (require) {
    "use strict";
    require('web.dom_ready');
    var attrs = JSON.parse($("input[name='prod_variants']").val());
    var attrs_dis = Object.assign(generateAttrDisplay(attrs));
    var isFinishFilter = false;
    $(document).on("click","#reset_variant",function() {
        resetToDefaultVariant($(this).closest('.js_product'));
    });
    $(document).on("click",".js_reset_variant",function() {
        resetToDefaultVariant($(this).closest('.js_product'));
    });
    $('.oe_website_sale').each(function (el) {
        var oe_website_sale = this;
        // filter attribute on loa
        filterAttributes(oe_website_sale);
        autoSelectDefaultVariant($(oe_website_sale).find('.js_product'));
        // auto fill on change
        var onChangeVariant = function(ele) {
              var $parent = $(ele).closest('.js_product');
                $parent.find("select.js_variant_change.always").each(function () {
                     //  auto filter attributes first
                     filterAttributes($parent);
                });
                let selection = ele;
                 let attr_name = $(selection).prev('.attribute_name').html();
                 let val = $(selection).val();
                 let attr_val = $(selection).find("option[value='"+ val +"']").attr("data-value_name");
                 //  auto match attributes
                 autoMatchAttributes({
                    'key': attr_name,
                    'value': attr_val,
                    'selection': selection
                 });
        }
        var isClick = false;
        $(document).on('click', 'select.js_variant_change.always', function (event) {
            if (isClick) {
                onChangeVariant(this)
            }
            isClick = !isClick;
        });

        $(document).on('focusout', 'select.js_variant_change.always', function (event) {
            isClick = false;
        });
    });


//    generate the priority of attributes
    function generateAttrDisplay(attrs){
         var attrs_d = {};
         if (attrs){
            $.each(attrs,function(indProd, prod){
                if (prod && prod.length > 0){
                     let proVariant = {};
                     $.each(prod[0],function(indAtt, att){
                        if(indAtt != 'seq_priority'){
                            proVariant[indAtt] = false;
                        }
                    });
                    attrs_d[indProd] = proVariant;
                }
            });
        }
        return attrs_d;
    }
//   reset to the top priority variant
     function resetToDefaultVariant(js_product){
        let v_attrs = $(js_product).find('.list-inline-item.variant_attribute');
        attrs_dis = Object.assign(generateAttrDisplay(attrs));
        autoSelectDefaultVariant(js_product);
        attrs_dis = Object.assign(generateAttrDisplay(attrs));
        v_attrs.find("select:not('.no_variant') option").show();
    }

//   select the top priority variant
    function autoSelectDefaultVariant(js_product){
         let product_id = $(js_product).find("input[class='product_template_id']").val();
         let v_attrs = $(js_product).find('.list-inline-item.variant_attribute');
         let p_attrs = attrs[product_id];
         if(p_attrs && p_attrs.length > 0){
//             get top priority variant
            let top_variant = p_attrs.reduce(function(prev, curr) {
                return prev.seq_priority < curr.seq_priority ? prev : curr;
            });
            $.each(top_variant, function(j, otVal) {
                 if($(v_attrs).find("select:not('.no_variant')").length > 0){
                     if(j != "seq_priority"){
                         let otValEscape = otVal.replace(/'/g, "\\'");
                         let corOption = $(v_attrs).find("option[data-attribute_name='" + j +"'][data-value_name='" + otValEscape +"']");
                         let sel = $(corOption).closest('select');
                         let val = $(corOption).val();
                         corOption.show();
                         $(sel).val(val);
                     }
                 }
            });
            let event = jQuery.Event( "change" );
            event.originalEvent = "originalEvent";
            $(js_product).find('.list-inline-item.variant_attribute select').eq(0).trigger(event)
         }
    }

//  auto filter attributes base on allow attributes values
    function autoMatchAttributes(params){
        if(params && params['key'] !== undefined && params['value'] !== undefined){
            let key = params['key'];
            let value = params['value'];
            let selection = params['selection'];
            var parent = $(selection).closest('.js_product');
            var product_id = $(parent).find("input[class='product_template_id']").val();
            var p_attrs = attrs[product_id];
            var p_attrs_dis = attrs_dis[product_id];
            p_attrs_dis[key] = value
            //hide all options which selected before
            let v_attrs = $(parent).find('.list-inline-item.variant_attribute');
            v_attrs.find("select:not('.no_variant') option").hide();
            $.each(p_attrs_dis, function(i, item) {
                if(i == key && item != false){
                    let otValEsc = value.replace(/'/g, "\\'");
                    v_attrs.find("option[data-attribute_name='" + key +"']").hide();
                    v_attrs.find("option[data-attribute_name='" + key +"'][data-value_name='" + otValEsc +"']").show();
                }
            });
            let p_allow_attrs = []
             $.each(p_attrs, function(i, item) {
                 let isMatch = true;
                 $.each(item, function(j, otVal) {
                    $.each(p_attrs_dis, function(k, dis) {
                        if(dis !== false && j == k && otVal != dis){
                            isMatch = false
                        }
                    });
                });
                if (isMatch){
                    p_allow_attrs.push(item)
                }
            });
            let cur_priority = -1;
            $.each(p_allow_attrs, function(i, item) {
                if(item.hasOwnProperty(key) && item[key] == value){
                    //  match with correct attributes
                    $.each(item, function(j, otVal) {
                         if($(v_attrs).find("select:not('.no_variant')").length > 0){
                             if(j != "seq_priority"){
                                 let otValEscape = otVal.replace(/'/g, "\\'");
                                 let corOption = $(v_attrs).find("option[data-attribute_name='" + j +"'][data-value_name='" + otValEscape +"']");
                                 let sel = $(corOption).closest('select');
                                 let val = $(corOption).val();
                                 corOption.show();
                                 if (cur_priority == -1 || cur_priority > item['seq_priority']){
                                     if($(corOption).css("display")==='block'){
                                        if($(sel)[0] != $(selection)[0]){
                                            $(sel).val(val);
                                        }
                                     }
                                 }
                             }
                         }
                    });
                    if (cur_priority == -1 || cur_priority > item['seq_priority']){
                        cur_priority = item['seq_priority']
                    }
                }
            });
            window.isFinishFilter = true;
        }
    }

//  filter attributes base on allow attributes values
    function filterAttributes(element){
       var oe_website_sale = element;
        if ($(element).closest('.oe_optional_products_modal').length > 0){
            oe_website_sale = $(element).closest('.oe_optional_products_modal');
        }
        $(oe_website_sale).find('select.js_variant_change.always').each(function () {
            let ele = this;
            let key = $(ele).closest('.list-inline-item.variant_attribute').attr('data-attribute_name');
            let options = $(ele).find("option");
            $.each(options, function(i, op) {
                let isMatch = false;
                var parent = $(this).closest('.js_product');
                var product_id = $(parent).find("input[class='product_template_id']").val();
                var p_attrs = attrs[product_id];
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

