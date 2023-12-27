# -- coding: utf-8 --
###################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2022-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Cybrosys (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request


class EmployeeChart(http.Controller):

    @http.route('/get/parent/colspan', type='json', auth='public', methods=['POST'], csrf=False)
    def get_col_span(self, job_id):
        if job_id:
            job_obj = request.env['hr.job'].sudo().browse(int(job_id))
            if job_obj.child_ids:
                child_count = len(job_obj.child_ids) * 2
                return child_count

    @http.route('/get/parent/job', type='json', auth='public', methods=['POST'], csrf=False)
    def get_job_ids(self):
        "funzione per recuperare la funzione aziendale all'apice"
        jobs = request.env['hr.job'].sudo().search([('parent_id', '=', False)])
        names = []
        key = []
        if len(jobs) == 1:
            key.append(jobs.id)
            key.append(len(jobs.child_ids))
            return key
        elif len(jobs) == 0:
            raise UserError(
                "Don't need to set manager to an employee at the top of the "
                "chart")
        else:
            for job in jobs:
                names.append(job.name)
            raise UserError(
                "These jobs have no upper job %s" % (names))

    def get_lines(self, loop_count):
        if loop_count:
            lines = """<tr class='lines'><td colspan='""" + str(loop_count) + """'>
                <div class='downLine'></div></td></tr><tr class='lines'>"""
            for i in range(0, loop_count):
                if i % 2 == 0:
                    if i == 0:
                        lines += """<td class="rightLine"></td>"""
                    else:
                        lines += """<td class="rightLine topLine"></td>"""
                else:
                    if i == loop_count-1:
                        lines += """<td class="leftLine"></td>"""
                    else:
                        lines += """<td class="leftLine topLine"></td>"""
            lines += """</tr>"""
            return lines

    def get_nodes(self, child_ids):
        if child_ids:
            child_nodes = """<tr>"""
            for child in child_ids:
                child_table = """<td colspan='""" + str(2) + """'>
                    <table><tr><td><div>"""
                view = """ <div id='""" + str(child.id) + """' class='o_level_1'><a>
                    <div id='""" + str(child.id) + """' class="o_employee_border">
                    </div>
                    <div class='employee_name'><p>""" + str(child.name) + """</p>
                    </div></a></div>"""
                child_nodes += child_table + view + """</div></td></tr></table></td>"""
            nodes = child_nodes + """</tr>"""
            return nodes

    @http.route('/get/parent/child', type='json', auth='user', methods=['POST'], csrf=False)
    def get_parent_child(self, job_id):
        """funzione per trovare le funzioni aziendali figli una funzione aziendale padre"""

        job_id = request.env['hr.job'].sudo().browse(job_id)
        child_job_ids = job_id.child_ids

        table = """<table><tr><td colspan='""" + str(len(child_job_ids) * 2) + """'><div class="node">"""
        view = """ <div id="parent" class='o_chart_head'><a>
            <div id='""" + str(job_id.id) + """' class="o_employee_border">
            </div>
            <div class='employee_name o_width'><p>""" + str(job_id.name) + """</p>
            </div></a></div>"""
        table += view + """</div></td></tr>"""
        loop_len = len(child_job_ids)*2
        lines = self.get_lines(loop_len)
        nodes = self.get_nodes(child_job_ids)
        table += lines + nodes
        return {'html': table, 'child_ids': child_job_ids.ids}

    @http.route('/get/child/data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_child_data(self, click_id):
        if click_id:
            job = request.env['hr.job'].sudo().browse(int(click_id))
            if job.child_ids:
                child_count = len(job.child_ids) * 2
                value = [child_count]
                lines = self.get_lines(child_count)
                nodes = self.get_nodes(job.child_ids)
                child_table = lines + nodes
                value.append(child_table)
                return {'html': child_table, 'child_ids': job.child_ids.ids, 'job_id': job.id, 'response': 'OK'}
        return {'response': 'KO'}






