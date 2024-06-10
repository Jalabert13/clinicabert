odoo.define('clinicabert2.script_name', function (require) {
    "use strict";

    var core = require('web.core');

    $(document).ready(function () {
        var urlParams = new URLSearchParams(window.location.search);
        var id = urlParams.get('id');

        // Realiza acciones basadas en el ID
        switch(id) {
            case "dashboard":
                console.log("dashboard");                                            
                break;
            case "profile":
                console.log("profile");                                            
                break;
            case "patients":
                console.log("patients");
                break;
            case "settings":
                console.log("settings");
                break;
            default:
                // Acción predeterminada en caso de que el ID no coincida
                break;
        }
    });
});