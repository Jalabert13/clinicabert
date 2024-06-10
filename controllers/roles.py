from odoo import http, models, api
from odoo.http import request

class RoleController(http.Controller):


    @http.route('/admin', type='http', auth='user', website=True)
    def roles(self, **kwargs):
        user = request.env.user
        if user.has_group('clinicabert2.custom_website_group'):
            return request.render('clinicabert2.template_custom_page')
        else:
            class UserGroups(models.Model):
                _inherit = 'res.users'

                @api.model
                def get_user_groups(self, user_id):
                    user = self.browse(user_id)
                    groups = user.groups_id
                    group_names = groups.mapped('name')
                    return group_names

            # return """
            #     <html>
            #         <head><title>Hola Mundo</title></head>
            #         <body>
            #             <h1>Hola Mundo!</h1>
            #             <p>Este es un párrafo en HTML.</p>
            #         </body>
            #     </html>
            #     """            
            # return request.redirect('/')

