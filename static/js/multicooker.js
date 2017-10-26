$(document).ready(function(){
  $.getJSON( "/api/recipes", function( data ) {
      var items = [];
      $.each( data.recipes, function( key, val ) {
          $('#select-recipes').append('<option value="' + val.url + '">'+val.name+'</option>');
      });     
  });
});

function handleSelect(elm)
{
  window.location = elm.value;
}