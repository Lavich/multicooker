$(document).ready(function(){
  $.getJSON( "/api/recipes", function( data ) {
      var items = [];
      $.each( data.recipes, function( key, val ) {
          $('#select-recipes').append('<option value="' + val.url + '">'+val.name+'</option>');
      });     
  });
});

function handleSelect(elm){
  createSteps(elm.value);
}

function createSteps(recipeUrl){
  $.getJSON(recipeUrl, function(data){
    var oldStep = $('.step');
    oldStep.remove();
    $.each( data.recipe.steps, function( key, val ) {
      $('#list-steps').append('<li class="step">'+val.id+'</li>');
    });     
  });
}