$(document).ready(function(){
    $.getJSON( "/api/recipes", function( data ) {
        var items = [];
        $.each( data.recipes, function( key, val ) {
            $('#select-recipes').append('<option>'+val.name+'</option>');
        });     
    });
});
