# project_management_advanced/__manifest__.py

{
    'name': 'Advanced Project Management System',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Manage projects, tasks, budgets, timelines, and resources.',
    'depends': ['base', 'project', 'hr', 'mail'],  # Dependencies on base, HR, project, and mail modules
    'data': [
        'security/ir.model.access.csv',  # Security rules
        'views/project_views.xml',  # Project, task, and milestone views
        'views/menu_items.xml',  # Menu items
        'data/cron_jobs.xml',  # Cron job data
        'report/project_report_templates.xml',  # PDF Report template
    ],
    'installable': True,
    'application': True,
}
