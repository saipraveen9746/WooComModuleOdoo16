from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _name = "purchase.requisition"
    _description = "Purchase Requisition"

    name = fields.Char(string='Purchase Requisition Number ', readonly=True, required=True, Copy=False, default='/')
    date = fields.Date(string="Requisition Date", default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', tracking=True)
    material_number = fields.Char(string='Material Number', readonly=True,)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', ondelete='restrict', )
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure',required=True)
    quantity = fields.Float(string='Quantity', )
    price = fields.Float(string='Rate', )
    price_total = fields.Float(string='Total', )
    wbs_grp_id = fields.Many2one("wbs.group", string="Wbs Group", )
    wbs_project_id = fields.Many2one("wbs.task", string="Wbs Project", )
    project_id = fields.Many2one("project.project", string="Project", )
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", )
    select = fields.Boolean(string="Select", default=False)
    po_req_id = fields.Many2one(
        comodel_name='purchase.order',
        readonly=True,
        index=True,
        auto_join=True,
        ondelete="cascade",
    )

    def action_approve(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.requisition.sequence') or 'New'
        result = super(PurchaseRequisition, self).create(vals)
        return result
