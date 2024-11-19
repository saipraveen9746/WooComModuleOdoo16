from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class ConstructionPurchaseOrderWizard(models.TransientModel):
    _name = "construction.purchase.order.wizard"
    _description = "Wizard for Selecting WBS Tasks"

    project_id = fields.Many2one("project.project", string="Project")
    sub_project_id = fields.Many2one("sub.project", string="Sub Project")
    wbs_project_id = fields.Many2one("wbs.task", string="WBS Project")
    start_date = fields.Date(string="From Date")
    end_date = fields.Date(string="To Date")
    requisition_ids = fields.Many2many("purchase.requisition", string="Approved Purchase Requisitions")
    partner_id = fields.Many2one("res.partner", string="Vendor", required=True)
    date_planned = fields.Datetime(string='Expected Arrival', index=True, store=True,)

    def search_purchase_requisition(self):
        domain = [('state', '=', 'approved')]
        if self.project_id:
            domain.append(('project_id', '=', self.project_id.id))
        if self.sub_project_id:
            domain.append(('sub_project_id', '=', self.sub_project_id.id))
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))

        purchase_requisitions = self.env['purchase.requisition'].search(domain)
        if purchase_requisitions:
            self.requisition_ids = [(6, 0, purchase_requisitions.ids)]
        else:
            raise UserError('No matching data found')

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'construction.purchase.order.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'name': 'Construction Search Purchase Requisitions',
        }

    def add_requisition_to_purchase_order(self):
        if not self.requisition_ids:
            raise UserError("No requisitions selected for creating a Purchase Order.")

        selected_requisitions = self.requisition_ids.filtered('select')
        if not selected_requisitions:
            raise UserError("Please select at least one requisition.")

        purchase_order = []
        for requisition in selected_requisitions:
            new_po = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'project_id': self.project_id.id,
                'sub_project_id': self.sub_project_id.id,
                'wbs_project_id': self.wbs_project_id.id,
                'po_requisition_lines': [(4, requisition.id)],
            })
            purchase_order.append(new_po)

            order_lines=self.env['purchase.order.line'].create({
                'name':requisition.product_id.display_name,
                'order_id': new_po.id,
                'product_id': requisition.product_id.id,
                'product_uom': requisition.product_uom_id.id,
                'product_qty': requisition.quantity,
                'price_unit': requisition.price,
                'partner_id':self.partner_id.id,
                'date_planned':fields.Datetime.now() + timedelta(days=7),

            })
            requisition.write({'state': 'done'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': purchase_order[0].id,
            'target': 'current',
            'name': 'Purchase Requisition',
        }
