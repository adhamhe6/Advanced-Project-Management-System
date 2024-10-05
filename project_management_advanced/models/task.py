# project_management_advanced/models/task.py

from odoo import models, fields, api

class ProjectTask(models.Model):
    _name = 'project.management.task'
    _description = 'Project Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Task Name', required=True, tracking=True)
    project_id = fields.Many2one('project.management', string='Project', ondelete='cascade', required=True)
    assigned_to = fields.Many2one('hr.employee', string='Assigned To')
    deadline = fields.Date(string='Deadline')
    milestone_id = fields.Many2one('project.management.milestone', string='Milestone')
    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('blocked', 'Blocked')
    ], string='Status', default='todo', tracking=True)
    description = fields.Text(string='Task Description')

    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        if task.assigned_to:
            task.message_subscribe([task.assigned_to.user_id.partner_id.id])
            task.message_post(body=f"Task assigned to {task.assigned_to.name}.")
        return task

    def action_start(self):
        self.state = 'in_progress'

    def action_done(self):
        self.state = 'done'
