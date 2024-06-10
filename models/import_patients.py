from odoo import models, fields
import csv
import io
import xmlrpc.client
from odoo import models, api
import base64

class ImportPatients(models.TransientModel):
    _name = 'clinica.import.patients'

    csv_file = fields.Binary(string="CSV File", required=True)


    @api.model
    def import_csv(self):
        url = 'http://localhost:8070'
        db = 'clinicabert'
        username = "juanjalabert03@gmail.com"
        password = "1243"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            decoded_csv = io.StringIO(base64.b64decode(self.csv_file).decode())
            csvreader = csv.reader(decoded_csv)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                gender = 'male' if row[2] == 'Male' else 'female'
                vals = {
                    'name': row[0],
                    'disability_type': row[1],
                    'diagnosis': row[2],
                    'entry_date': row[3],
                    'gender': gender,
                    'weight': float(row[5]),
                    'height': float(row[6]),
                    'location': row[7],
                    'birth_date': row[8],
                    'report': row[9],
                    'contact_phone': row[10],
                }
                create_id = models.execute_kw(db, uid, password, 'clinica.patient', 'create', [vals])
                print("create record ->", create_id)