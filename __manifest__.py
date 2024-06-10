{
    'name': 'Modulo para Clinicas de Discapacidades',
    'author': 'Juan Jalabert Riquelme.',
    'summary': 'Modulo para personas con discapacidades desarrollado en 2024.',
    'depends': ['base', 'base_import', 'mail'],
    'data': [
        'security/ir.model.access.csv',

        'views/patient.xml',
        'views/menu.xml',
        'views/filter.xml',
        'views/template.xml',
        'views/admin.xml',
        'views/admin_layout.xml',
        'views/admin_security.xml',
        'views/import_patient.xml',


        'data/group_data.xml',
        'data/patient_data.xml'
    ],
'assets': {
        'web.assets_frontend': [
            'clinicabert2/static/assets/js/show_single_patient.js',
            'clinicabert2/static/assets/js/fill_map.js',
            'clinicabert2/static/assets/js/active_link.js',



            'clinicabert2/static/assets/css/style.css',



        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}