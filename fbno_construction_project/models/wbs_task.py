from odoo import models, fields, api


class WbsTask(models.Model):
    _name = "wbs.task"
    _description = "For creating WBS task"

    name = fields.Char(string="WBS Name", required=True)
    project_id = fields.Many2one("project.project", string="Project")
    sub_project_id = fields.Many2one("sub.project", string="Sub Project")
    wbs_task_group_ids = fields.One2many("wbs.group", 'wbs_grp_id', string="WBS Groups")


class WbsGroup(models.Model):
    _name = "wbs.group"
    _description = "For creating WBS groups"

    name = fields.Char(string="WBS Group", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    wbs_grp_id = fields.Many2one(
        string='WBS Project',
        comodel_name='wbs.task',
        index=True,
        auto_join=True,
        ondelete="cascade",
    )
    task_library_ids = fields.One2many("project.task.library", 'task_ids', string="Task Library")
    project_id = fields.Many2one("project.project", string="Project", compute="_compute_project_and_subproject",
                                 store=True)
    sub_project_id = fields.Many2one("sub.project", string="Sub Project", compute="_compute_project_and_subproject",
                                     store=True)

    @api.depends('task_library_ids')
    def _compute_task_count(self):
        for record in self:
            record.labour_line_count = len(record.task_library_ids)

    @api.depends('wbs_grp_id')
    def _compute_project_and_subproject(self):
        for record in self:
            if record.wbs_grp_id:
                record.project_id = record.wbs_grp_id.project_id
                record.sub_project_id = record.wbs_grp_id.sub_project_id
            else:
                record.project_id = False
                record.sub_project_id = False
