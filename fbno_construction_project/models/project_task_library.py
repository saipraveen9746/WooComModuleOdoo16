from odoo import models, fields, api


class ProjectTaskLibrary(models.Model):
    _name = "project.task.library"
    _description = "For creating task libraries"

    name = fields.Char(string="Task Title", required=True)
    category = fields.Char(string="Category")
    minimum_quantity = fields.Float(string="Minimum Quantity")
    sub_category = fields.Char(string="Sub Category")
    unit_id = fields.Many2one("uom.uom", string="Unit")
    material_lines_ids = fields.One2many("task.material.lines", 'material_id', string="Material Lines")
    labour_lines_ids = fields.One2many("construction.labour.lines", 'labour_id', string="Labour Lines")
    task_ids = fields.Many2one(
        comodel_name='wbs.group',
        index=True,
        auto_join=True,
        ondelete="cascade",
    )
    project_id = fields.Many2one("project.project", string="Project", compute="_compute_project_and_subproject",
                                 store=True)
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", compute="_compute_project_and_subproject",
                                     store=True)

    @api.depends('material_lines_ids.price', 'material_lines_ids.quantity')
    def _compute_total_material_cost(self):
        for record in self:
            total = sum(line.price * line.quantity for line in record.material_lines_ids)
            record.total_material_cost = total

    total_material_cost = fields.Float(string="Total Material Cost", compute="_compute_total_material_cost", store=True)

    @api.depends('labour_lines_ids.rate', 'labour_lines_ids.quantity')
    def _compute_total_labour_cost(self):
        for record in self:
            total = sum(line.rate * line.quantity for line in record.labour_lines_ids)
            record.total_labour_cost = total

    total_labour_cost = fields.Float(string="Total Labour Cost",compute="_compute_total_labour_cost", store=True )
    material_line_count = fields.Integer(string="Material Lines", compute="_compute_material_line_count", store=True)
    labour_line_count = fields.Integer(string="Labour Lines", compute="_compute_labour_line_count", store=True)

    @api.depends('material_lines_ids')
    def _compute_material_line_count(self):
        for record in self:
            record.material_line_count = len(record.material_lines_ids)

    @api.depends('labour_lines_ids')
    def _compute_labour_line_count(self):
        for record in self:
            record.labour_line_count = len(record.labour_lines_ids)

    @api.depends('task_ids')
    def _compute_project_and_subproject(self):
        for record in self:
            if record.task_ids:
                record.project_id = record.task_ids.project_id
                record.sub_project_id = record.task_ids.sub_project_id
            else:
                record.project_id = False
                record.sub_project_id = False