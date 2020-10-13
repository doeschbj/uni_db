function start_auto_func() {
  //alert("Auto wird gestartet");
  var selected = this.id;
  var status_field = document.getElementById('status_field');
  switch (selected) {
  case "start_auto":
    status_field.innerHTML = 'Auto wird gestartet';
    addList("Auto");
    break;
  case "start_lkw":
    status_field.innerHTML = 'Lkw wird gestartet';
    addList("Lkw");
    break;
  case "start_motor":
    status_field.innerHTML = 'Motorrad wird gestartet';
    addList("Motorrad");
    break;
  case "start_anhanger":
    status_field.innerHTML = 'Anhänger wird gestartet';
    addList("Anhänger");
    break;
  case "stop":
    status_field.innerHTML = 'Stopping';
  break;
  case "rmv_list":
    removeFromList(1);
  break;
  default:
    break;
}
}
function addList(eintrag) {
  var li = document.createElement("li");
  li.appendChild(document.createTextNode(eintrag));
  alist.appendChild(li);
}
function removeFromList(i){
  if(alist.childNodes[i] != undefined){
    alist.removeChild(alist.childNodes[i])
    if(alist.childNodes[i] == undefined){
      status_field.innerHTML = 'Inaktiv';
    }
  }else{
    status_field.innerHTML = 'Inaktiv';
  }
}

var start_auto  = document.getElementById('start_auto');
var start_lkw  = document.getElementById('start_lkw');
var start_mtrrad  = document.getElementById('start_motor');
var start_anhanger = document.getElementById('start_anhanger');
var rmv_list  = document.getElementById('rmv_list');
var stop  = document.getElementById('stop');
var alist = document.getElementById('auftragsliste');
start_auto.addEventListener ('click', start_auto_func, true);
start_lkw.addEventListener ('click', start_auto_func, true);
start_mtrrad.addEventListener ('click', start_auto_func, true);
start_anhanger.addEventListener ('click', start_auto_func, true);
stop.addEventListener ('click', start_auto_func, true);
rmv_list.addEventListener('click', start_auto_func, true);
