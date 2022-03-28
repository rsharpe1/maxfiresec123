/** @odoo-module **/

/*
This file includes few snippets related to storing/clearing information about workstation
printers/scales. A bit 'hacky' thing :)
*/

import rpc from 'web.rpc';
import session from 'web.session';
import { browser } from '@web/core/browser/browser';

import WORKSTATION_DEVICES from './constants';

// Remove information about workstation printers from localStorage when logout
const currentUserId = session.uid;
const storageUserId = browser.localStorage.getItem('printnode_base.user_id');

// If not user found in localStorage or user changed - clean workstation devices
if (!storageUserId || (currentUserId != parseInt(storageUserId))) {
    for (let workstationDevice of WORKSTATION_DEVICES) {
        browser.localStorage.removeItem('printnode_base.' + workstationDevice);
    }
}

// Save current user in localStorage
browser.localStorage.setItem('printnode_base.user_id', currentUserId);

// Check if devices with IDs from localStorage exists
const devicesInfo = Object.fromEntries(
    WORKSTATION_DEVICES
        .map(n => [n, browser.localStorage.getItem('printnode_base.' + n)])  // Two elements array
        .filter(i => i[1]) // Skip empty values
);

rpc.query({
    model: 'res.users',
    method: 'validate_device_id',
    kwargs: { devices: devicesInfo }
}).then((data) => {
    // We have to copy context to variable, change it and then assign back because of
    // limitations of Odoo source code
    let userContext = session.user_context;

    // Remove bad device IDs from localStorage
    for (const workstationDevice in data) {
        if (data[workstationDevice]) {
            // ID is correct, place in session
            let workstationDeviceId = browser.localStorage.getItem(
                'printnode_base.' + workstationDevice);

            if (workstationDeviceId) {
                // Add information about printer to user context
                userContext[workstationDevice] = workstationDeviceId;
            }
        } else {
            // Remove from localStorage
            browser.localStorage.removeItem('printnode_base.' + workstationDevice);
        }

        // Replace context with updated object
        Object.defineProperties(session, {
            user_context: {
                value: userContext,
                configurable: true,
            },
        });
    }
});
