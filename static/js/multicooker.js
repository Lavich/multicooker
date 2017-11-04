
var recipesViewModel = new RecipesViewModel();
var stepViewModel = new StepViewModel();


window.onload = function () {
  ko.applyBindings(recipesViewModel, $('#main')[0]);
  ko.applyBindings(stepViewModel, $('#step')[0]);
}


function RecipesViewModel() {
  var self = this;
  self.apiURI = window.location.href + 'api';
  self.steps = ko.observableArray();
  self.recipe_list = ko.observableArray();
  self.recipe = ko.observable();

  self.ajax = function(uri, method, data) {
    var request = {
      url: uri,
      type: method,
      contentType: "application/json",
      accepts: "application/json",
      cache: false,
      dataType: 'json',
      data: data
      // JSON.stringify(data)
    };
    return $.ajax(request);
  }

  self.updateListRecipes = function(){
    self.ajax(self.apiURI + '/recipes', 'GET').done(function(data) {
      for (var i = 0; i < data.recipes.length; i++) {
        self.recipe_list.push(data.recipes[i].name);
      };
    });
  }
  self.updateListRecipes(); 


  self.updateSteps = function(){
    self.ajax(self.apiURI + '/recipes/' + self.recipe(), 'GET').done(function(data) {
      self.steps([]);
      for (var i = 0; i < data.steps.length; i++) {
        self.steps.push({
          recipe_name: ko.observable(data.steps[i].recipe_name),
          id: ko.observable(data.steps[i].id),
          time: ko.observable(data.steps[i].time),
          temperature: ko.observable(data.steps[i].temperature),
          wait: ko.observable(data.steps[i].wait),
          description: ko.observable(data.steps[i].description),

        });
      };
    });
  };

  self.beginAdd = function(step)
  {
    $('#step').modal('show');
    stepViewModel.id('');
    stepViewModel.recipe_name(self.recipe());
  }

  self.beginEdit = function(step)
  {
    $('#step').modal('show');
    stepViewModel.id(step.id());
    stepViewModel.recipe_name(step.recipe_name());
    stepViewModel.description(step.description());
    stepViewModel.time(step.time());
    stepViewModel.temperature(step.temperature());
    stepViewModel.wait(step.wait());
  }

  self.stepSave = function(step) {
    var url = 'api/steps';
    var method = 'POST';
    if (step.id) {
      url += '/' + step.id;
      method = 'PUT';
    }
    console.log(url);
    self.ajax(url, method, step).done(function(data) {
      console.log(data);
      if (data.step.recipe_name == self.recipe_name) {
        self.steps.push({
          recipe_name: ko.observable(data.step.recipe_name),
          id: ko.observable(data.step.id),
          time: ko.observable(data.step.time),
          temperature: ko.observable(data.step.temperature),
          wait: ko.observable(data.step.wait),
          description: ko.observable(data.step.description),
        });
      }
      else{
        self.recipe_list.push(data.step.recipe_name);
        self.updateSteps();
      }
    });
  }

  self.remove = function(step) {
    console.log(step.id());
    self.ajax('api/steps/' + step.id(), 'DELETE').done(function() {
      self.steps.remove(step);
    });
  }
}

function StepViewModel() {
  var self = this;
  self.id = ko.observable('');
  self.recipe_name = ko.observable();
  self.description = ko.observable('');
  self.time = ko.observable('');
  self.temperature = ko.observable('');
  self.wait = ko.observable('');

  self.save = function() {
    $('#step').modal('hide');
    recipesViewModel.stepSave({
      id: self.id(),
      recipe_name: self.recipe_name(),
      description: self.description(),
      time: self.time(),
      temperature: self.temperature(),
      wait: self.wait(),
    });
  }

}
