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
      }
    }
  });

  var interval = setInterval(function(){
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
};
