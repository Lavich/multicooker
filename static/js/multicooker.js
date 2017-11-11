window.onload = function () {
  var heater = new Vue({
    el: '#heater',
    data: {
      timeLeft: 110,
      timeSet: 200,
      tempNow: 100,
      tempSet: 200,
      isStart: false,
    },
    computed: {
      timeLeftHour: function () {
        return Math.floor(this.timeLeft / 60) + ":" + this.timeLeft % 60;
      },
      timeSetHour: function () {
        return Math.floor(this.timeSet / 60) + ":" + this.timeSet % 60;
      }
    },
    methods: {
      start: function () {
        var params = new URLSearchParams();
        params.append('temp_set', this.tempSet);
        params.append('time_set', this.timeSet);
        axios.post('/start', params);
      },
      stop: function () {
        axios.post('/stop');
      },
    }
  });

  var intervalID = setInterval(function(){
    axios.get('/status')
    .then(function(response) {
      console.log(response.data);
      heater.tempNow = Math.round(response.data['temp_now']), 1;
        // heater.tempSet = response.data['temp_set'];
        heater.timeLeft = response.data['time_left'];
        heater.isStart = response.data['is_start'];
      })
    ;}, 
    1000);

  Vue.use(VueCharts);
  var pid = new Vue({
    el: '#pid',
    data:{
      isStart: false,
      pTerm:[10,22,30],
      iTerm:[1,5,3],
      dTerm:[0,4,0],
      labels:['','',''],
    },
    methods: {
      start: function () {
        this.isStart = true;
        setInterval(update(), 1000);
      },
      stop: function () {
        isStart = false;
        clearInterval(intervalPID);
      },
      update: function () {
        axios.get('/pid')
        .then(function(response) {
          console.log(response.data);
          this.pid.pTerm.push(response.data['p_term']);
          this.iTerm.push(response.data['i_term']);
          this.dTerm.push(response.data['d_term']);
        })
      }
    }
  });

function update() {
        axios.get('/pid')
        .then(function(response) {
          console.log(response.data);
          console.log(response.data['p_term']);
          // pid.pTerm.push(response.data['p_term']);
          // pid.iTerm.push(response.data['i_term']);
          // pid.dTerm.push(response.data['d_term']);
          pid.labels.push('');
        })   
}
  
};