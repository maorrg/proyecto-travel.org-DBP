
function get_experienciasDevExtream(){
    var url = "http://127.0.0.1:8000/experiencias";
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
             dataField: "titulo"
         }, {
             dataField: "descripcion"
         }, {
             dataField: "precio"
         }, {
            dataField: "fecha"
         }, {
             dataField: "calificacion"
         }, {
             dataField: "guia_id"
         }]
     }).dxDataGrid("instance");
}