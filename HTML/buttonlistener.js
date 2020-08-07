function start_auto_func() {
  //alert("Auto wird gestartet");
  var selected = this.id;
  var status_field = document.getElementById('status_field');
  switch (selected) {
  case "start_auto":
    status_field.innerHTML = 'Auto wird gestartet';
    break;
  case "start_lkw":
    status_field.innerHTML = 'Lkw wird gestartet';
    break;
  case "start_motor":
    status_field.innerHTML = 'Motorrad wird gestartet';
    break;
  case "start_nothing":
    status_field.innerHTML = 'Nichts wird gestartet';
    break;
  case "stop":
    status_field.innerHTML = 'Stopping';
  break;
  default:
    break;
}


 }

var start_auto  = document.getElementById('start_auto');
var start_lkw  = document.getElementById('start_lkw');
var start_mtrrad  = document.getElementById('start_motor');
var start_nothing  = document.getElementById('start_nothing');
var stop  = document.getElementById('stop');
start_auto.addEventListener ('click', start_auto_func, true);
start_lkw.addEventListener ('click', start_auto_func, true);
start_mtrrad.addEventListener ('click', start_auto_func, true);
start_nothing.addEventListener ('click', start_auto_func, true);
stop.addEventListener ('click', start_auto_func, true);
