from odoo import models, fields, api


class WbsTaskWizard(models.TransientModel):
    _name = "wbs.task.wizard"
    _description = "Wizard for Selecting WBS Tasks"

    project_id = fields.Many2one("project.project", string="Project")
    sub_project_id = fields.Many2one("sub.project", string="Sub Project")
    wbs_grp_ids = fields.Many2one('wbs.group', string='Task Results')
    material_lines_ids = fields.Many2many('task.material.lines', string="Material Lines")
    labour_lines_ids = fields.Many2many('construction.labour.lines', string="Labour Lines")

    def search_wbs_tasks(self):
        domain = []
        if self.project_id:
            domain.append(('project_id', '=', self.project_id.id))
        if self.sub_project_id:
            domain.append(('sub_project_id', '=', self.sub_project_id.id))
        if self.wbs_grp_ids:
            domain.append(('task_ids', '=', self.wbs_grp_ids.id))

        tasks = self.env['project.task.library'].search(domain)
        material_lines = tasks.mapped('material_lines_ids')
        material_lines.write({'select': False})

        self.material_lines_ids = [(6, 0, material_lines.ids)]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wbs.task.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'name': 'Search WBS Tasks',
        }

    def add_material_lines_to_requisition(self):
        selected_material_lines = self.material_lines_ids.filtered('select')  # Get selected material lines
        if selected_material_lines:
            purchase_requisitions = []
            for line in selected_material_lines:
                requisition = self.env['purchase.requisition'].create({
                    'date': fields.Date.context_today(self),
                    'state': 'draft',
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom_id.id,
                    'quantity': line.quantity,
                    'price': line.price,
                    'price_total': line.price_total,
                    'wbs_grp_id': line.wbs_grp_id.id,
                    'wbs_project_id': line.wbs_project_id.id,
                    'project_id': line.project_id.id,
                    'sub_project_id': line.sub_project_id.id,
                    'material_number': line.name,
                })
                purchase_requisitions.append(requisition.id)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.requisition',
                'view_mode': 'form',
                'res_id': purchase_requisitions[0],
                'target': 'current',
                'name': 'Purchase Requisition',
            }

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