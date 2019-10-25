
function get_viajerosDevExtream(){
    var url = "http://127.0.0.1:8000/viajeros";
     $("#grid").dxDataGrid({
         dataSource: DevExpress.data.AspNet.createStore({
             key: "id",
             insertUrl: url,
             updateUrl: url,
             deleteUrl: url,
             loadUrl: url,
             onBeforeSend: function(method, ajaxOptions) {
                 ajaxOptions.xhrFields = { withCredentials: true };
             }
         }),

         editing: {
             allowUpdating: true,
             allowDeleting: true,
             allowAdding: true
         },

         remoteOperations: {
             sorting: true,
             paging: true
         },

         paging: {
             pageSize: 12
         },

         pager: {
             showPageSizeSelector: true,
             allowedPageSizes: [8, 12, 20]
         },

         columns: [{
             dataField: "id",
             dataType: "number",
             allowEditing: false
         }, {
             dataField: "nombre"
         }, {
             dataField: "apellido"
         }, {
             dataField: "correo"
         }, {
             dataField: "usuario"
         }, {
             dataField: "contrasena"
         }, {
             dataField: "edad"
         }, {
             dataField: "pais"
         } ]
     }).dxDataGrid("instance");



}