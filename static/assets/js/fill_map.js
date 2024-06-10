odoo.define('clinicabert2.fill_map', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var LocationUpdater = Widget.extend({
        init: function() {
            var self = this;
            self._super.apply(this, arguments);
            document.addEventListener('DOMContentLoaded', function() {
                self.updateMapLocation();
            });
        },

        updateMapLocation: function() {
            var patientLocationValue = document.querySelector('input[name="patient_location"]').value;
            console.log("Valor de patient.location:", patientLocationValue);

            var mapIframe = document.querySelector('.s_map_embedded');
            if (mapIframe && patientLocationValue.trim() !== "") {
                var newSrc = 'https://maps.google.com/maps?q=' + encodeURIComponent(patientLocationValue) + '&t=m&z=12&ie=UTF8&iwloc=&output=embed';
                mapIframe.setAttribute('src', newSrc);
            } else {
                console.log("No se pudo encontrar el iframe o el valor de patient.location está vacío");
            }
        },
    });

    return LocationUpdater;
});
