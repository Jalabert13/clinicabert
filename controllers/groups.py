from odoo import http
from odoo.http import request

class MyModule(http.Controller):

    @http.route('/user_groups', type='json', auth="user")
    def user_groups(self):
        user = request.env.user
        group_names = [group.name for group in user.groups_id]
        return group_names
