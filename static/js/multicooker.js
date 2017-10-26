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
  $.getJSON( elm.value, function( data ) {
    var items = [];
    var myNode = $('.step');
    myNode.remove();
    $.each( data.recipe.steps, function( key, val ) {
      $('#list-steps').append('<li class="step">'+val.id+'</li>');
    });     
  });
}