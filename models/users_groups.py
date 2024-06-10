from odoo import models, api

class UserGroups(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_user_groups(self, user_id):
        user = self.browse(user_id)
        groups = user.groups_id
        group_names = groups.mapped('name')
        return group_names