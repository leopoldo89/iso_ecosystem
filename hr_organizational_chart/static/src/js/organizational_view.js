odoo.define('hr_organizational_chart.view_chart', function (require){
"use strict";
console.log("hlooooooooo")
var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var _t = core._t;


var EmployeeOrganizationalChart =  AbstractAction.extend({

    contentTemplate: 'OrganizationalEmployeeChart',
    events: {
        'click img': '_getChild_data',
        'click .employee_name': 'view_employee',
    },

    init: function(parent, context) {
        this.checked_ids = []
        this._super(parent, context);
        this.renderEmployeeDetails();
    },
    renderEmployeeDetails: function (){
        var employee_id = 1
        var self = this;
        console.log("hhhhh",this)
        this._rpc({
            route: '/get/parent/job',
        }).then(function (result) {
            self.parent_len = result[1];
            self._rpc({
                route: '/get/parent/child',
                params: {
                    job_id: parseInt(result[0]),
                },
            }).then(function (value){

                $('#o_parent_employee').append(value['html']);
                self.checked_ids.push(result[0])
                for(var i = 0;i < value['child_ids'].length; i++){
                    if(!self.checked_ids.includes(value['child_ids'][i])){
                        self._getChild_data(value['child_ids'][i]);
                        self.checked_ids.push(value['child_ids'][i]);
                    }
                }

            });

        });

    },
    _getChild_data: function(id){

        if(id){
            var self = this
            this.id = id;
            this.check_child =  $( "#"+this.id+".o_level_1" );
            if (this.check_child[0]){
                this.colspan_td = this.check_child[0].parentElement.parentElement
                this.tbody_child = this.colspan_td.parentElement.parentElement
                var child_length = this.tbody_child.children.length
                if (child_length == 1){
                    this._rpc({
                        route: '/get/parent/colspan',
                        params: {
                            job_id: parseInt(this.id),
                        },
                    }).then(function (col_val){
                        if (col_val){
                            self.colspan_td.colSpan = col_val;
                        }
                    });
                    this._rpc({
                        route: '/get/child/data',
                        params: {
                            click_id: parseInt(this.id),
                        },
                    }).then(function (result){
                        if (result['response'] == 'OK'){

                            var check_child =  $( "#" + result['job_id'] + ".o_level_1" );
                            if (check_child[0]) {
                                var colspan_td = check_child[0].parentElement.parentElement
                                colspan_td.colSpan = result['child_ids'].length*2
                                var tbody_child = colspan_td.parentElement.parentElement
                                $(result['html']).appendTo(tbody_child);
                                self.checked_ids.push(result['job_id'])
                                for(var i = 0;i < result['child_ids'].length; i++) {
                                    if (!self.checked_ids.includes(result['child_ids'][i])) {
                                        self._getChild_data(result['child_ids'][i]);
                                        self.checked_ids.push(result['child_ids'][i]);
                                    }
                                }
                            }
                        }
                    });
                }
                else{
                    for(var i = 0;i < 3; i++){
                        this.tbody_child.children[1].remove();
                    }
                    self.colspan_td.colSpan = 2;
                }

            }
        }
    },
    view_employee: function(ev){
        console.log("viiii")
        if (ev.target.parentElement.className){
            var id = parseInt(ev.target.parentElement.parentElement.children[0].id)
            this.do_action({
            name: _t("job"),
            type: 'ir.actions.act_window',
            res_model: 'hr.job',
            res_id: id,
            view_mode: 'form',
            views: [[false, 'form']],
            })
        }
    },
});
    core.action_registry.add('organization_dashboard', EmployeeOrganizationalChart);

});
