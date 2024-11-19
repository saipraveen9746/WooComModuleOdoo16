from odoo import models, fields, api

class LabourLines(models.Model):
    _name = 'construction.labour.lines'
    _description = 'Labour Lines for Construction Projects'

    select = fields.Boolean(string="Select", default=False)
    name = fields.Char(string='Labour Number', readonly=True, required=True, Copy=False, default='New')
    labour_id =  fields.Many2one(comodel_name='project.task.library',required=True,readonly=True,index=True,auto_join=True,ondelete="cascade",)
    labour_type_id = fields.Many2one('construction.labour.type', string="Labour", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    rate = fields.Float(string="Rate per Unit", default=1.0)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)
    wbs_grp_id = fields.Many2one("wbs.group", string="Wbs Group", compute="_compute_wbs_project_and_wbs_group",store=True)
    wbs_project_id = fields.Many2one("wbs.task", string="Wbs Project", compute="_compute_wbs_project_and_wbs_group", store=True)
    project_id = fields.Many2one("project.project", string="Project", compute="_compute_project_and_subproject", store=True)
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", compute="_compute_project_and_subproject", store=True)

    @api.depends('quantity', 'rate')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.rate

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('construction.labour.lines.sequence') or '/'
        result = super(LabourLines,self).create(vals)
        return result

    @api.depends('labour_id')
    def _compute_wbs_project_and_wbs_group(self):
        for record in self:
            if record.labour_id:
                record.wbs_grp_id = record.labour_id.task_ids
                record.wbs_project_id = record.labour_id.task_ids.wbs_grp_id
            else:
                record.wbs_grp_id = False
                record.wbs_project_id = False


class LabourType(models.Model):
    _name = 'construction.labour.type'
    _description = 'Types of Labour'

    name = fields.Char(string="Labour Type", required=True)
