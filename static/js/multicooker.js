window.onload = function () {
  var stepsViewModel = new StepsViewModel();
  ko.applyBindings(stepsViewModel, $('#main')[0]);
  stepsViewModel.updateRecipes();
  stepsViewModel.updateSteps('Pasta');
}

function stripTrailingSlash(str) {
  if(str.substr(-1) === '/') {
    return str.substr(0, str.length - 1);
  }
  return str;
}

function StepsViewModel() {
  var self = this;
  self.apiURI = window.location.href + 'api';
  self.steps = ko.observableArray();
  self.recipes = ko.observableArray();

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

  self.updateRecipes = function(){
    self.ajax(self.apiURI + '/steps', 'GET').done(function(data) {
      self.recipes(data.recipes)
    });

  }

  self.updateSteps = function(nameRecipe){
    self.ajax(self.apiURI + '/steps/' + nameRecipe, 'GET').done(function(data) {
      console.log(data.steps)
      self.steps([]);
      for (var i = 0; i < data.steps.length; i++) {
        console.log(data.steps[i].recipe_name);
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
  }

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

