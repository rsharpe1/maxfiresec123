/** @odoo-module **/

import FormController from 'web.FormController';
import FormView from 'web.FormView';
import rpc from 'web.rpc';
import viewRegistry from 'web.view_registry';
import session from 'web.session';

import { browser } from '@web/core/browser/browser';

import WORKSTATION_DEVICES from './constants';

const ResUsersPreferencesFormController = FormController.extend({
    _onButtonClicked: function (event) {
        this._super.apply(this, arguments);

        const attrs = event.data.attrs;

        if (attrs.name === 'preference_save') {
            // Update local printer
            const record = event.data.record;

            for (let workstationDeviceAttr of WORKSTATION_DEVICES) {
                const workstationDeviceField = record.data[workstationDeviceAttr];

                if (workstationDeviceField) {
                    const workstationDeviceId = workstationDeviceField.data.id;

                    // Save in localStorage for future use
                    browser.localStorage.setItem('printnode_base.' + workstationDeviceAttr, workstationDeviceId);

                    // Update context to send with every request
                    session.user_context[workstationDeviceAttr] = workstationDeviceId;

                } else {
                    // Clean localStorage
                    browser.localStorage.removeItem('printnode_base.' + workstationDeviceAttr);

                    // Remove from user context
                    delete session.user_context[workstationDeviceAttr];
                }
            }
        }

    },
});

const ResUsersPreferencesView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: ResUsersPreferencesFormController,
    }),

    _loadData: async function (model) {
        return Promise.all([
            this._super.apply(this, arguments),
            this._validateWorkstationDevices()  // Hack to clean wrong device IDs
        ]).then((result) => { return result[0]; });
    },

    _validateWorkstationDevices: function () {
        // Check if devices with IDs from localStorage exists
        const devicesInfo = Object.fromEntries(
            WORKSTATION_DEVICES
                .map(n => [n, localStorage.getItem('printnode_base.' + n)])  // Two elements array
                .filter(i => i[1]) // Skip empty values
        );

        return rpc.query({
            model: 'res.users',
            method: 'validate_device_id',
            kwargs: { devices: devicesInfo }
        }).then((data) => {
            // Remove bad device IDs from localStorage
            for (const workstationDevice in data) {
                if (data[workstationDevice]) {
                    // ID is correct, place in session
                    let workstationDeviceId = browser.localStorage.getItem(
                        'printnode_base.' + workstationDevice);

                    if (workstationDeviceId) {
                        // Add information about printer to user context
                        session.user_context[workstationDevice] = workstationDeviceId;
                    }
                } else {
                    // Remove from localStorage
                    browser.localStorage.removeItem('printnode_base.' + workstationDevice);
                }
            }
        });
    }
});


viewRegistry.add('printnode_res_users_preferences_form', ResUsersPreferencesView);

export default ResUsersPreferencesView;
