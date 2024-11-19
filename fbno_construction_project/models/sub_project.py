from odoo import models, fields, api


class SubProject(models.Model):
    _name = 'sub.project'
    _description = 'For Sub Projects'

    name = fields.Char(string="Name", required=True)
    project_id = fields.Many2one("project.project", string="Project", )
    budget_applicable = fields.Boolean(string="Budget Applicable",default=False)
