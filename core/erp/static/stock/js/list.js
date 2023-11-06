$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "cat.name"},
            {"data": "tipo.name"},
            {"data": "image"},
            {"data": "estado"},
            {"data": "stock"},

        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-2], // Esta columna representa el estado del producto
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var iconHTML = '';
            
                    if (data === true) { // Comparar con valor booleano en lugar de cadena
                        iconHTML = '<i class="fas fa-check fa-lg rounded-circle text-success"></i>';
                    } else {
                        iconHTML = '<i class="fas fa-times fa-lg rounded-circle text-danger"></i>';
                    }
            
                    return iconHTML;
                }
            },

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.stock <= 5) {
                        return '<span class="badge badge-danger">' + data + '</span>';
                    } else if (row.stock > 5 && row.stock <= 15) {
                        return '<span class="badge badge-warning">' + data + '</span>';
                    } else {
                        return '<span class="badge badge-success">' + data + '</span>';
                    }
                }
            },

        ],
        initComplete: function (settings, json) {

        }
    });
});



