from odoo import models, fields

class PatientImage(models.Model):
    _name = 'patient.image'
    _description = 'Patient Image'

    name = fields.Char(string='Name')
    image = fields.Binary(string='Image')
    patient_id = fields.Many2one('clinica.patient', string='Patient')