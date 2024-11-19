from odoo import models, fields
from odoo.exceptions import UserError


class PurchaseOrderExtend(models.Model):
    _inherit = "purchase.order"
    _description = "Purchase order for Construction Management"

    project_id = fields.Many2one("project.project", string="Project", )
    sub_project_id = fields.Many2one("sub.project", string="Sub Project" )
    wbs_grp_id = fields.Many2one("wbs.group", string="Wbs Group", )
    wbs_project_id = fields.Many2one("wbs.task", string="Wbs Project")
    po_requisition_lines = fields.One2many('purchase.requisition','po_req_id', string="Purchase Order Requisition Lines")
    date_planned = fields.Datetime(
        string='Expected Arrival', index=True,
        compute="_compute_price_unit_and_date_planned_and_name", readonly=False, store=True,
        help="Delivery date expected from vendor. This date respectively defaults to vendor pricelist lead time then today's date.")

    def add_requisition_purchase_order(self):
        if self.project_id and self.sub_project_id and self.wbs_project_id:
            vendor = self.partner_id
            if not vendor:
                raise UserError("Please select a Vendor for the Purchase Order.")
            purchase_order_wizard = self.env['construction.purchase.order.wizard'].create({
                'project_id': self.project_id.id,
                'wbs_project_id': self.wbs_project_id.id,
                'sub_project_id': self.sub_project_id.id,
                'partner_id': vendor.id,
                'date_planned': self.date_planned
            })
            print(purchase_order_wizard,'purchase order wizard')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Construction Purchase Order Wizard',
            'res_model': 'construction.purchase.order.wizard',
            'view_mode': 'form',
            'res_id': purchase_order_wizard.id,
            'target': 'new',  # 'new' opens in a popup window
        }

    def action_view_picking(self):
        res = super(PurchaseOrderExtend, self).action_view_picking()
        print(res,'res')
