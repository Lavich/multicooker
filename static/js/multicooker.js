window.onload = function () {

  var recipesViewModel = new RecipesViewModel();
  ko.applyBindings(recipesViewModel, $('#main')[0]);
}


function RecipesViewModel() {
  var self = this;
  self.apiURI = window.location.href + 'api';
  self.steps = ko.observableArray();
  self.recipe_list = ko.observableArray();
  self.recipe = ko.observable('Latvia');

  self.ajax = function(uri, method, data) {
    var request = {
      url: uri,
      type: method,
      contentType: "application/json",
      accepts: "application/json",
      cache: false,
      dataType: 'json',
      data: JSON.stringify(data)
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
          temperature: ko.observable(data.steps[i].temp),
          wait: ko.observable(data.steps[i].wait),
          description: ko.observable(data.steps[i].description),

        });
      };
    });
  };

  self.edit = function(task, data) {
    self.ajax(task.uri(), 'PUT', data).done(function(res) {
      self.updateTask(task, res.task);

    });
  }

  self.beginAdd = function()
  {
    $('#add').modal('show');
  }
  self.beginEdit = function(steps) {
    alert("Edit: " + steps.id());
  }
  self.remove = function(steps) {
    alert("Remove: " + steps.id());
  }
  self.markInProgress = function(task) {
    task.done(false);
  }
  self.markDone = function(task) {
    task.done(true);
  }
}

