from odoo import models, fields, api

class QueryView(models.TransientModel):
    _name = 'query.view'
    _description = 'Querys SQL'

    query = fields.Text(string='Query')
    query_text = fields.Text(string='Texto de la consulta', readonly=True)

    def execute_query(self):
        query = self.query
        if query:
            self._cr.execute(query)
            query_results = self._cr.fetchall()
            result_text = '\n'.join(','.join(map(str, row)) for row in query_results)
            self.write({'query_text': result_text})
        else:
            self.write({'query_text': ''})
        # Reload the view
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
