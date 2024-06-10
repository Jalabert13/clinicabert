from odoo import http
from odoo.http import request
from functools import wraps
from odoo.http import request


class Busqueda(http.Controller):
     
    @http.route('/patients', website=True, auth='public')
    def mostrarPacientesFiltrados(self, **kw):
        disability_type = request.params.get('disability_type')
        association = request.params.get('association')
        location = request.params.get('location')

        domain = []
        if disability_type:
            domain.append(('disability_type', 'ilike', disability_type))
        if association:
            domain.append(('association.name', 'ilike', association))
        if location:
            domain.append(('location', 'ilike', location))

        patients = request.env['clinica.patient'].sudo().search(domain)

        # Get unique values ​​for select options
        all_patients = request.env['clinica.patient'].sudo().search([])
        
        # Extract unique disability types, associations, and locations
        disability_typees = {patient.disability_type.strip().lower() for patient in all_patients if isinstance(patient.disability_type, str) and patient.disability_type.strip()}
        associations = {patient.association.name.strip().lower() for patient in all_patients if patient.association and isinstance(patient.association.name, str) and patient.association.name.strip()}
        locations = {patient.location.strip().lower() for patient in all_patients if isinstance(patient.location, str) and patient.location.strip()}


        
        return http.request.render('clinicabert2.filtro_busqueda_pacientes', {
            'patients': patients,  # Renamed 'animals' to 'patients' for clarity
            'disability_typees': disability_typees,
            'associations': associations,
            'locations': locations,
            'selected_disability_type': disability_type,
            'selected_association': association,
            'location': location,
        })
                


    @http.route('/patient/<int:patient_id>', type='http', auth='public', website=True)
    def mostrar_mascota(self, patient_id):
            pet = request.env['clinica.patient'].sudo().browse(patient_id)

            if not pet:
                return """
                    <html>
                        <head><title>Error</title></head>
                        <body>
                            <h1>Error: Paciente no encontrado</h1>
                            <p>Lo sentimos, No se ha encontrado ningun paciente que corresponda a la búsqueda.</p>
                        </body>
                    </html>
                """
            
            return http.request.render('clinicabert2.patient_single', {'patient': pet})
        
    def admin_image(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = request.env.user
            image_data = user.image_1920

            if image_data:
                # Detect file format
                if image_data[:4] == b'\x89PNG':
                    mime_type = 'image/png'
                elif image_data[:2] == b'\xff\xd8':
                    mime_type = 'image/jpeg'
                elif image_data[:4] == b'<svg':
                    mime_type = 'image/svg+xml'
                else:
                    mime_type = 'image/png'  # Default MIME type
                
                image_base64 = image_data.decode('utf-8')
            else:
                image_base64 = None
                mime_type = None
            
            context = {
                'image_base64': image_base64,
                'mime_type': mime_type,
            }
            return func(*args, admin_image=context, **kwargs)
        return wrapper


    @http.route(['/admin','/admin/profile','/admin/patients'], website=True, auth='user')
    @admin_image
    def show_admin_panel(self, admin_image, **kw):
        current_route = request.httprequest.path
        user = request.env.user
        patients = request.env['clinica.patient'].search([('association', '=', user.id)])
        return request.render('clinicabert2.is_admin', {'current_route': current_route, 'admin_image': admin_image, 'patients': patients})
    