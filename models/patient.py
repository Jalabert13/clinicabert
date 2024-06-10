import logging
import csv
import io
import base64
import xmlrpc.client

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class ClinicaPatient(models.Model):
    _name = "clinica.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Registro de pacientes con discapacidad"

    name = fields.Char(string="Nombre", required=True)
    disability_type = fields.Char(string="Tipo de Discapacidad")
    diagnosis = fields.Char(string="Diagnóstico")
    entry_date = fields.Date(string="Fecha de Ingreso")
    gender = fields.Selection([('Masculino', 'Masculino'), ('Femenino', 'Femenino')], string="Género")
    weight = fields.Float(string="Peso")
    height = fields.Float(string="Altura")
    location = fields.Char(string="Localidad")
    birth_date = fields.Date(string="Fecha de Nacimiento")
    image = fields.Image(string="Imagen", compute_sudo=True, required=True)
    age = fields.Char(string="Edad", compute='_compute_age')
    association = fields.Many2one('res.users', string="Asociación", readonly=True, default=lambda self: self.env.user)
    report = fields.Text(string="Informe")
    contact_phone = fields.Char(string="Teléfono de contacto")
    state = fields.Selection([('available', 'Disponible'),
                              ('in_process', 'En proceso'),
                              ('treated', 'Tratado')], default='available', string="Estado del Tratamiento")
    image_ids = fields.One2many('patient.image', 'patient_id', string='Images')

    csv_file = fields.Binary(string="CSV File", required=True)

    groups_id = fields.Char(string="Id de grupo")
    ad_group_name = "Bert-Administracion"



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

    @api.depends('birth_date')
    def _compute_age(self):
        today = datetime.now().date()
        for patient in self:
            if patient.birth_date:
                delta = today - patient.birth_date
                years = delta.days // 365
                months = delta.days % 365 // 30
                days = delta.days % 30
                if years < 1:
                    if months == 0:
                        patient.age = "{} días".format(days)
                    else:
                        patient.age = "{} meses y {} días".format(months, days)
                else:
                    patient.age = "{} años".format(years)
            else:
                patient.age = "Desconocido"



    @api.model
    def action_view_pet(self, id):
        id = str(id).strip('[]')
        
        target_url = f"http://localhost:8069/patient/{id}"

        logger.info("Redirigiendo a: %s", target_url)
        
        return {
            'type': 'ir.actions.act_url',
            'url': target_url,
            'target': 'self',
        }
    


    @api.model
    def obtener_id_por_nombre(self, ad_group_name):
        grupo = self.env['res.groups'].search([('name', '=', ad_group_name)], limit=1)
        if grupo:
            return grupo.id
        else:
            return False
        

