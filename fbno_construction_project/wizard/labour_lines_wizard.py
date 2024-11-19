from odoo import models, fields, api


class LabourTaskWizard(models.TransientModel):
    _name = "labour.task.wizard"
    _description = "Wizard for Selecting Labours Tasks"

    project_id = fields.Many2one("project.project", string="Project")
    sub_project_id = fields.Many2one("sub.project", string="Sub Project")
    wbs_grp_ids = fields.Many2one('wbs.group', string='Task Results')
    labour_lines_ids = fields.Many2many('construction.labour.lines', string="Labour Lines")

    def search_labour_lines(self):
        domain = []
        if self.project_id:
            domain.append(('project_id', '=', self.project_id.id))
        if self.sub_project_id:
            domain.append(('sub_project_id', '=', self.sub_project_id.id))
        if self.wbs_grp_ids:
            domain.append(('task_ids', '=', self.wbs_grp_ids.id))

        tasks = self.env['project.task.library'].search(domain)
        labour_lines = tasks.mapped('labour_lines_ids')
        labour_lines.write({'select': False})

        self.labour_lines_ids = [(6, 0, labour_lines.ids)]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wbs.task.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'name': 'Search Labour Lines',
        }