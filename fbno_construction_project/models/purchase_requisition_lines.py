from odoo import models, fields, api


class PurchaseOrderRequisitionLines(models.Model):
    _name = "purchase.requisition.lines"
    _description = "Purchase Order Requisition Lines"

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
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure')
    quantity = fields.Float(string='Quantity', )
    price = fields.Float(string='Rate', )
    price_total = fields.Float(string='Total', )
    wbs_grp_id = fields.Many2one("wbs.group", string="Wbs Group", )
    wbs_project_id = fields.Many2one("wbs.task", string="Wbs Project", )
    project_id = fields.Many2one("project.project", string="Project", )
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", )
    select = fields.Boolean(string="Select", default=False)