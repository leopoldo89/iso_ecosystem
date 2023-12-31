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
        """funzione per recuperare la funzione aziendale all'apice
            utilizzata solo dal primo livello"""
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
        """funzione per creare le linee di collegamento tra le funzioni aziendali"""
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
        """funzione di renderizzazione dei figli di una funzine aziendale """

        if child_ids:
            child_nodes = """<tr>"""
            for child in child_ids:
                sigla_fa = ""
                if child.sigla_fa:
                    sigla_fa = ' (' + child.sigla_fa + ')'
                employee_list = self.get_fa_employee_ids(child)
                child_table = """<td colspan='""" + str(2) + """'>
                    <table class='mx-auto'><tr><td><div>"""
                view = """
                    <div id='""" + str(child.id) + """' class='o_level_1'>
                        <div id='""" + str(child.id) + """' class="o_employee_border"></div>
                        <div class='border d-inline-block p-4'>
                            <h2>""" + str(child.name) + sigla_fa +"""</h2>""" + employee_list + """
                        </div>
                    </div>"""
                child_nodes += child_table + view + """</div></td></tr></table></td>"""
            nodes = child_nodes + """</tr>"""
            return nodes

    @http.route('/get/parent/child', type='json', auth='user', methods=['POST'], csrf=False)
    def get_parent_child(self, job_id):
        """funzione per trovare le funzioni aziendali figlie una funzione aziendale padre.
         utilizzata solo dal primo livello"""

        job_id = request.env['hr.job'].sudo().browse(job_id)
        child_job_ids = job_id.child_ids
        sigla_fa = ""
        if job_id.sigla_fa:
            sigla_fa = ' (' + job_id.sigla_fa + ')'
        employee_list = self.get_fa_employee_ids(job_id)
        table = """<table><tr><td colspan='""" + str(len(child_job_ids) * 2) + """'><div class="node">"""
        view = """<div id="parent" class='o_chart_head'>
                        <div id='""" + str(job_id.id) + """' class="o_employee_border"></div>
                        <div class='border d-inline-block p-4'>
                            <h2>""" + str(job_id.name) + sigla_fa +"""</h2>""" + employee_list + """
                        </div>
                    </div>"""
        table += view + """</div></td></tr>"""
        loop_len = len(child_job_ids)*2
        lines = self.get_lines(loop_len)
        nodes = self.get_nodes(child_job_ids)
        table += lines + nodes
        return {'html': table, 'child_ids': child_job_ids.ids}

    def get_fa_employee_ids(self, job_id):
        """funzione che genera la lista di dipendenti che appartengono ad una certa funzione aziendale"""

        html_list = "<ul style='list-style:none; padding:0;'>"
        mansioni_svolte = request.env['hr.job.svolta'].sudo().search([('employee_id', '!=', False), ('job_id', '=', job_id.id)])
        employee_ids = []
        for mansione in mansioni_svolte:
            if mansione.employee_id.id not in employee_ids and mansione.employee_id.name:
                html_list += "<li>" + mansione.employee_id.name + "</li>"
                employee_ids.append(mansione.employee_id.id)
        html_list += "</ul>"
        return html_list

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






