# project_management_advanced/models/project.py

from odoo import models, fields, api
from datetime import timedelta

class Project(models.Model):
    _name = 'project.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Advanced Project Management'

    name = fields.Char(string='Project Name', required=True)
    project_manager_id = fields.Many2one('res.users', string='Project Manager')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Project Description')
    budget = fields.Float(string='Project Budget')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    task_ids = fields.One2many('project.management.task', 'project_id', string='Tasks')
    milestone_ids = fields.One2many('project.management.milestone', 'project_id', string='Milestones')
    resource_ids = fields.Many2many('hr.employee', string='Assigned Resources')
    budget_spent = fields.Float(string='Spent Budget', compute='_compute_budget_spent')

    @api.depends('task_ids')
    def _compute_budget_spent(self):
        """ Compute the total budget spent based on assigned resources to tasks """
        for project in self:
            project.budget_spent = sum(task.assigned_to.contract_id.wage for task in project.task_ids)

    def action_start(self):
        self.state = 'in_progress'

    def action_complete(self):
        self.state = 'completed'

    def _cron_project_deadline_reminder(self):
        """ Sends reminders if project deadline is nearing """
        today = fields.Date.today()
        projects = self.search([('end_date', '!=', False), ('state', '=', 'in_progress')])
        for project in projects:
            if project.end_date and project.end_date - today <= timedelta(days=3):
                project.message_post(
                    body=f"Reminder: Project {project.name} is nearing its deadline.",
                    subtype="mail.mt_comment"
                )
