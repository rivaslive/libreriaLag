$(function () {

    $('#art').click(function (e) {
        var nombre, codigo, stock, cajas;
        nombre = $("#id_nombre_articulo").val();
        codigo = $("#id_codigo_articulo").val();
        stock = $("#id_stock").val();
        cajas = $("#id_stock_caja").val();
         
        limpiar();
        
        var onlyText = /^[a-zA-ZáéíóúàèìòùÀÈÌÒÙÁÉÍÓÚñÑüÜ\s]+$/;
        var onlyInt = /^[0-9]+(.[0-9]+)?$/;

        if (nombre === "" || codigo === "" || stock === "" || cajas === "") {
            e.preventDefault();
            $("#id_nombre_articulo").addClass("error");
            $("#id_codigo_articulo").addClass("error");
            $("#id_stock").addClass("error");
            $("#id_stock_caja").addClass("error");
            return false;
        } else if (nombre === null || !onlyText.test(nombre)) {
            e.preventDefault();
            $("#id_nombre_articulo").addClass("error");
            alert("Ingrese un Nombre valido");
            return false;
        } else if (codigo === null || !codigo.match(onlyInt)) {
            e.preventDefault();
            $("#id_codigo_articulo").addClass("error");
            alert("Ingrese un Codigo valido");
            return false;
        } else if (stock === null || !stock.match(onlyInt)) {
            e.preventDefault();
            $("#id_stock").addClass("error");
            alert("Ingrese un numero valido");
            return false;
        }
        else if (!cajas.match(onlyInt)) {
            e.preventDefault();
            $("#id_stock_caja").addClass("error");
            alert("Ingrese un numero valido");
            return false;
        }
        return $("#form").submit();
    });
    function limpiar(){
        $("#id_nombre_articulo").removeClass("error");
        $("#id_codigo_articulo").removeClass("error");
        $("#id_stock").removeClass("error");
        $("#id_stock_caja").removeClass("error");
    }
});