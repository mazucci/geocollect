function getToday() {
  var today = new Date();

  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();

  if(dd<10)
    dd='0'+dd;

  if(mm<10)
    mm='0'+mm;

  today = yyyy+'-'+mm+'-'+dd;
  return today;
}

function getTodayMinusTwoDays(){
  var today = new Date();

  var dd = today.getDate() - 2;
  var yyyy = today.getFullYear();
  if (today.getDate() < 3)
    var mm = today.getMonth();
  else
    var mm = today.getMonth()+1;

  if(dd<10)
    dd='0'+dd;

  if(mm<10)
    mm='0'+mm;

  var todayMinusTwoDays = yyyy+'-'+mm+'-'+dd;
  return todayMinusTwoDays;
}

console.log(getToday() + " --- " + getTodayMinusTwoDays());
