import logging
import csv
import io
import base64

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class ClinicaImportCsv(models.Model): 
    _name = "clinica.import.csv"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    import_file = fields.Binary(string="Archivo de Importación", attachment=True)
    file_name = fields.Char(string="Nombre del Archivo")

    def import_data(self):
        if not self.import_file:
            raise UserError(_("Por favor, cargue un archivo para importar."))

        try:
            # Decodificar el archivo binario
            file_content = io.StringIO(base64.decodebytes(self.import_file))

            # Leer el archivo CSV
            reader = csv.reader(file_content, delimiter=',', quotechar='"')
            for line in reader:
                # Procesar cada línea del archivo CSV
                # Suponiendo que la primera línea del archivo CSV contiene los encabezados de columna
                if reader.line_num == 1:
                    # Ignorar la primera línea (encabezados de columna)
                    continue

                # Procesar los datos de la línea actual
                # Ejemplo: crear un nuevo registro de paciente
                name = line[0]  # Suponiendo que el primer campo es el nombre
                disability_type = line[1]  # Suponiendo que el segundo campo es el tipo de discapacidad
                # Aquí puedes crear un nuevo registro de paciente con los datos de la línea actual
                # Ejemplo: self.create({'name': name, 'disability_type': disability_type, ...})
        except Exception as e:
            # Manejar cualquier error que ocurra durante la importación
            error_msg = _("Error importing record: %s") % str(e)
            logger.error(error_msg)
            raise UserError(error_msg)
        
        # Devolver acción para cerrar la ventana de importación después de completar
        return {'type': 'ir.actions.act_window_close'}
