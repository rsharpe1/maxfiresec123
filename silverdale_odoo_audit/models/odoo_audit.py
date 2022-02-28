# -*- coding: utf-8 -*-

from operator import is_
import subprocess
from odoo import models, fields, api, _
import os
from odoo.exceptions import ValidationError
import base64

INSTALLED_DOMAIN = [('state', '=', 'installed')]

STATE_SELECTION = [
    ('draft', 'draft'),
    ('processing', 'Processing'),
    ('ready', 'Ready'),
    ('printed', 'Printed'),
    ('cancel', 'Cancelled'),
    ('retry', 'Retry'),
]


class OdooAudit(models.Model):
    _name = 'odoo.audit'
    _inherit = ['portal.mixin']
    _order = 'id desc'
    _description = 'Odoo Audit'

    name = fields.Char(default='Draft', copy=False)
    industry_id = fields.Many2one('res.partner.industry')
    user_id = fields.Many2one('res.users', string="Audit By", default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    date = fields.Datetime('Datetime', default=fields.Datetime.now)
    state = fields.Selection(STATE_SELECTION, default='draft')
    # Data fields
    master_data = fields.Text()
    duplicate_count = fields.Text()
    report_data = fields.Text()
    # For pylint data store in txt file
    tech_data = fields.Text()
    tech_file = fields.Binary()
    tech_file_name = fields.Char()
    # Store report in this field
    audit_report = fields.Binary('File')
    file_name = fields.Char('File name')
    # parameters
    is_installed_app_chart = fields.Boolean(string="Installed App Chart", default=True)
    is_installed_app_list = fields.Boolean(string="Installed App List", default=True)
    is_categ_app = fields.Boolean(string="Installed App Category", default=True)
    is_master_data = fields.Boolean(string="Show Master Data", default=True)
    is_group_role = fields.Boolean(string="Show Security Roles", default=True)
    is_duplicated_count = fields.Boolean(string="Duplicated Count", default=True)
    is_tech_data = fields.Boolean(string="Code Quality", default=False)
    is_tech_data_ready = fields.Boolean(string="Technical Data Ready")
    is_manifest_data = fields.Boolean(string="Manifest details", default=False)
    is_company_config = fields.Boolean(string="Company Configuration")
    is_system_config = fields.Boolean(string="System Configuration")

    def action_run_report(self):
        """Run report"""
        if self.name == 'Draft':
            self.name = self.env['ir.sequence'].next_by_code('odoo.audit')

        if self.is_duplicated_count:
            self.get_duplicated_data()

        if self.is_group_role:
            self.get_user_role()

        if self.is_master_data:
            self.get_master_data()

        self.state = "ready"

        if self.is_tech_data:
            self.state = "processing"
            self.generate_technical_data()

    def refresh_data(self):
        """Refresh form view when state in progress."""

        return {
            'tag': 'reload',
        }

    def get_master_data(self):
        """
        Get master dataset from audit.master.data
        save json data in master_data field
        """

        records = self.env['audit.master.data'].sudo().search([])
        data = {}
        for rec in records:
            data_set = {}
            data_set['Total'] = self.env[rec.name.model].sudo().search_count([])
            for line in rec.domain_line:
                data_set[line.name] = self.env[line.model_id].sudo().search_count(eval(line.domain))

            data[rec.name.name] = data_set
        self.master_data = data

    def get_duplicated_data(self):
        """ Get duplicated data using odoo api"""

        records = self.env['duplicate.data.count'].sudo().search([])
        data = {}

        for rec in records:
            data_set = {}

            total_rec = self.env[rec.name.model].sudo().search_count([])
            data_set['Total'] = total_rec
            for line in rec.duplicate_data_line:
                model = rec.name.model
                key = line.field_description

                duplicated = len(self.env[model].sudo().read_group([(line.name, '!=', False)], [line.name], line.name))
                empty_record = self.env[model].sudo().search_count([(line.name, '=', False)])
                data_set[key] = total_rec - duplicated - empty_record

            data[rec.name.name] = data_set

        self.duplicate_count = data

    def get_eval(self, data):
        """Send back eval data
        """
        if data:
            return eval(data)
        return []

    # TODO make it generic
    def get_master_data_json(self):
        """return eval data to report."""

        return eval(self.master_data)

    # TODO make it generic
    def get_pylint_data(self):
        """Decode base64 data into string"""

        return base64.b64decode(self.tech_file)

    def get_installed_app_chart(self):
        """Get report data when click on view button"""

        data = {}
        apps = self.env['ir.module.module']
        total_apps = apps.sudo().search_count(INSTALLED_DOMAIN)
        installed_apps = apps.sudo().read_group(INSTALLED_DOMAIN, ['author'], 'author')

        values = [x['author_count'] for x in installed_apps]
        labels = [x['author'].title() for x in installed_apps]
        data_parse = dict()
        for i, j in zip(labels, values):
            print("ssss")
            if i in data_parse:
                data_parse[i] = data_parse[i] + j
            else:
                data_parse.update({i: j})
        # data_parse = {i: j for i, j in zip(lables, values)}
        return (data_parse, total_apps)

    def get_installed_app_catg_chart(self):
        """ Return category chart for pdf report"""

        data = {}
        apps = self.env['ir.module.module']
        installed_apps = apps.read_group(INSTALLED_DOMAIN, ['category_id'], 'category_id')

        values = [x['category_id_count'] for x in installed_apps]
        labels = [x['category_id'][1][:] if x['category_id'] else "Undefined" for x in installed_apps]

        total = 0
        for i in values:
            total = total + int(i)
        data_parse = dict()
        for i, j in zip(labels, values):
            if i in data_parse:
                data_parse[i] = data_parse[i] + j
            else:
                data_parse.update({i: j})

        # data_parse = {i: j for i, j in zip(labels, values)}
        return (data_parse, total)

    def get_installed_app_list(self):
        """ Return installed application list"""

        domain = [('state', '=', 'installed')]
        data = self.env['ir.module.module'].sudo().search(domain, order='author')
        return data

    def get_company_config_data(self):
        """ Show company data"""
        data = {}
        company_id = self.env['ir.model'].sudo().search(
            [('model', '=', 'res.company')], limit=1).id
        fields = self.env['ir.model.fields'].sudo().search(
            [('model_id', '=', company_id)], order='modules desc')
        dic = {}

        for field in fields:
            if dic.get(field.modules, False) != field.modules:
                dic[field.modules] = 'Module'
            data = eval("self.company_id.{}".format(field.name))

            if field.ttype in ['boolean', 'char', 'float', \
                               'interger', 'reference', 'selection', 'text']:
                dic[field.field_description] = data
            elif field.ttype in ['many2one']:
                if len(data) == 1:
                    dic[field.field_description] = data.name

        return dic

    def get_user_role(self):
        """
            return [
                'User Name':['grp1','grp1','grp1',...],
                'User Name2':['grp1','grp1','grp1',...]]
        """

        data = []
        users = self.env['res.users'].sudo().search([])

        for user in users:
            groups = user.groups_id.read_group(
                [('users', 'in', user.id)],
                ['category_id'],
                'category_id'
            )
            values = [x['category_id'][1][:] if x['category_id'] else "Undefined" for x in groups]
            data_set = {}
            data_set[user.name] = values
            data.append(data_set)
        return data

    def get_system_config_data(self):
        """ ---- """
        dic = {}
        values = self.env['ir.config_parameter'].sudo().search([])
        for val in values:
            if 'database' not in val.key:
                dic[val.key] = val.value
        return dic

    def generate_technical_data(self):
        """Generat txt file for pylint report using bash"""

        self.get_portal_url()

        report_location = self.env['ir.config_parameter'].sudo().get_param(
            'silversale_odoo_audit.technical_report_location')

        if not os.path.isdir(report_location):
            try:
                os.mkdir(report_location)
            except OSError:
                raise ValidationError(_("Cannot create a dir for reports"))

        url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        url += "/audit/report/{}?access_token={}&db={}".format(
            self.id, self.access_token, self._cr.dbname)

        module_location = os.path.dirname(os.path.realpath(__file__))
        addons_path = self.env['audit.addons.list'].sudo().search([])
        bash_path = module_location + '/bash.sh'
        pylintrc = module_location + '/pylintrc'

        tmp = report_location + "/{}_temp.txt".format(self.id)
        out = report_location + "/{}_data.txt".format(self.id)

        for addons in addons_path:
            process = subprocess.Popen("bash {} -p {} -t {} -o {} -c {} -u {}".format(
                bash_path, addons.name, tmp, out, pylintrc, url).split(),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE
                                       )

        self.state = 'processing'

    def print_report(self):
        """Print and save report"""
        report_name = 'silverdale_odoo_audit.action_report_odoo_auit_report'
        data, data_format = self.env.ref(report_name)._render_qweb_pdf(self.id)
        audit_report = base64.encodestring(data)
        self.write({
            'audit_report': audit_report,
            'file_name': self.name.replace('/', '_'),
            'state': 'printed'
        })
        return self.env.ref(report_name).report_action(self)
