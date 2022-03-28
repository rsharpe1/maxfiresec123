/** @odoo-module **/

import fieldRegistry from 'web.field_registry';
import { browser } from '@web/core/browser/browser';
import { FieldMany2One } from 'web.relational_fields';


const WorkstationDeviceField = FieldMany2One.extend({
    start: function () {
        this._super.apply(this, arguments);

        // Update value of workstation
        let workstationDeviceId = browser.localStorage.getItem('printnode_base.' + this.name);

        if (workstationDeviceId) {
            this._setValue(workstationDeviceId);
        }
    },
});

fieldRegistry.add('printnode_res_users_workstation_device_many2one', WorkstationDeviceField);

export default WorkstationDeviceField;
