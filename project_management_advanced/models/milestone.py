# project_management_advanced/models/milestone.py

from odoo import models, fields

class ProjectMilestone(models.Model):
    _name = 'project.management.milestone'
    _description = 'Project Milestone'

    name = fields.Char(string='Milestone Name', required=True)
    project_id = fields.Many2one('project.management', string='Project', ondelete='cascade', required=True)
    due_date = fields.Date(string='Due Date')
    description = fields.Text(string='Milestone Description')
