from odoo import models, fields, api


class TaskMaterialLines(models.Model):
    _name = "task.material.lines"
    _description = "For creating task material lines"

    name = fields.Char(string='Material Number', readonly=True, required=True, Copy=False, default='/')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        ondelete='restrict',
    )
    product_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
    )
    quantity = fields.Float(
        string='Quantity',
    )
    price = fields.Float(
        string='Rate',
    )
    price_total = fields.Float(
        string='Total',
        compute='_compute_totals', store=True,
    )
    material_id = fields.Many2one(
        comodel_name='project.task.library',
        required=True,
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
    )
    wbs_grp_id = fields.Many2one("wbs.group", string="Wbs Group", compute="_compute_wbs_project_and_wbs_group",
                                     store=True)
    wbs_project_id = fields.Many2one("wbs.task", string="Wbs Project", compute="_compute_wbs_project_and_wbs_group",
                                 store=True)
    project_id = fields.Many2one("project.project", string="Project", compute="_compute_project_and_subproject",
                                 store=True)
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", compute="_compute_project_and_subproject",
                                     store=True)
    select = fields.Boolean(string="Select", default=False)

    @api.depends('price', 'quantity')
    def _compute_totals(self):
        for line in self:
            line.price_total = line.price * line.quantity

    @api.depends('material_id')
    def _compute_wbs_project_and_wbs_group(self):
        for record in self:
            if record.material_id:
                record.wbs_grp_id = record.material_id.task_ids
                record.wbs_project_id = record.material_id.task_ids.wbs_grp_id
            else:
                record.wbs_grp_id = False
                record.wbs_project_id = False

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('task.material.lines.sequence') or '/'
        result = super(TaskMaterialLines,self).create(vals)
        return result
