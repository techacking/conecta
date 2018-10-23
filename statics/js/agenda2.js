var Cal = function(divId) {

  //Store div id
  this.divId = divId;

  // Days of week, starting on Sunday
  this.DaysOfWeek = [
    'Dom',
    'Seg',
    'Ter',
    'Qua',
    'Qui',
    'Sex',
    'Sab'
  ];

  // Months, stating on January
  this.Months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ];

  // Set the current month, year
  var d = new Date();

  this.currMonth = d.getMonth();
  this.currYear = d.getFullYear();
  this.currDay = d.getDate();

};

// Goes to next month
Cal.prototype.nextMonth = function() {
  if ( this.currMonth == 11 ) {
    this.currMonth = 0;
    this.currYear = this.currYear + 1;
  }
  else {
    this.currMonth = this.currMonth + 1;
  }
  this.showcurr();
};

// Goes to previous month
Cal.prototype.previousMonth = function() {
  if ( this.currMonth == 0 ) {
    this.currMonth = 11;
    this.currYear = this.currYear - 1;
  }
  else {
    this.currMonth = this.currMonth - 1;
  }
  this.showcurr();
};

// Show current month
Cal.prototype.showcurr = function() {
  this.showMonth(this.currYear, this.currMonth);
};

// Show month (year, month)
Cal.prototype.showMonth = function(y, m) {

  var d = new Date()
  // First day of the week in the selected month
  , firstDayOfMonth = new Date(y, m, 1).getDay()
  // Last day of the selected month
  , lastDateOfMonth =  new Date(y, m+1, 0).getDate()
  // Last day of the previous month
  , lastDayOfLastMonth = m == 0 ? new Date(y-1, 11, 0).getDate() : new Date(y, m, 0).getDate();


  var html = '<table class="shadow">';

  // Write selected month and year
  html += '<thead><tr>';
  html += '<td colspan="7" class="rounded bg-success text-white">' + this.Months[m] + ' ' + y + '</td>';
  html += '</tr></thead>';


  // Write the header of the days of the week
  html += '<tr class="days">';
  for(var i=0; i < this.DaysOfWeek.length;i++) {
    html += '<td>' + this.DaysOfWeek[i] + '</td>';
  }
  html += '</tr>';

  // Write the days
  var i=1;
  do {

    var dow = new Date(y, m, i).getDay();

    // If Sunday, start new row
    if ( dow == 0 ) {
      html += '<tr>';
    }
    // If not Sunday but first day of the month
    // it will write the last days from the previous month
    else if ( i == 1 ) {
      html += '<tr>';
      var k = lastDayOfLastMonth - firstDayOfMonth+1;
      for(var j=0; j < firstDayOfMonth; j++) {
        html += '<td class="bg-light">'+ k + '</td>';
        k++;
      }
    }

	//Escreve os eventos
	function mostrarEventos(y, m, d, listEvents) {
          var passo;
          var events = []
          for (passo = 0; passo < listEvents.length; passo++) {
            var datahoraI = listEvents[passo]['startdate'].split("-");
            var anoI = datahoraI[0];
            var mesI = datahoraI[1];
            var diaI = datahoraI[2].substring(0, 2);
			var datahoraF = listEvents[passo]['enddate'].split("-");
            var anoF = datahoraI[0];
            var mesF = datahoraI[1];
            var diaF = datahoraI[2].substring(0, 2);
            if (anoI <= y.toString() && y.toString() <= anoF && mesI <= (parseInt(m, 10) + 1).toString() && (parseInt(m, 10) + 1).toString() <= mesF && diaI <= d.toString() && d.toString() <= diaF) {
				if (events.length < 3){
					events.push('<tr><td><button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#testModalEvent">'+listEvents[passo]['title']+'</button></td></tr>');
				} else if (events.length == 3) {
					events[events.length - 1] = '<tr><td><button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#testModalEvent">+'+(events.length - 2).toString()+' Eventos</button></td></tr>';
				}
            }
          }
		  while (events.length < 3){
			  events.push('<tr><td><button type="button" class="invisible btn btn-info btn-block">ifdhyfgusdf</button></td></tr>');
		  }
	  return events.join('') + '</table>';
	}

    // Write the current day in the loop
    var chk = new Date();
    var chkY = chk.getFullYear();
    var chkM = chk.getMonth();
    if (chkY == this.currYear && chkM == this.currMonth && i == this.currDay) {
      html += '<td class="rounded bg-success text-white"><table><tr><td class="daysNumber">' + i + '</td></tr>' + mostrarEventos(this.currYear,this.currMonth,i,eventos) + '</a></td>';
    } else {
      html += '<td><a role="button" class="btn btn-primary btn-block" data-toggle="modal" href="#exampleModalCenter"><table><tr><td class="daysNumber">' + i + '</td></tr>' + mostrarEventos(this.currYear,this.currMonth,i,eventos) + '</a></td>';
    }
    // If Saturday, closes the row
    if ( dow == 6 ) {
      html += '</tr>';
    }
    // If not Saturday, but last day of the selected month
    // it will write the next few days from the next month
    else if ( i == lastDateOfMonth ) {
      var k=1;
      for(dow; dow < 6; dow++) {
        html += '<td class="bg-light">' + k + '</td>';
        k++;
      }
    }

    i++;
  }while(i <= lastDateOfMonth);

  // Closes table
  html += '</table>';

  // Write HTML to the div
  document.getElementById(this.divId).innerHTML = html;
};

// On Load of the window
window.onload = function() {

  // Start calendar
  var c = new Cal("divCal");			
  c.showcurr();

  // Bind next and previous button clicks
  getId('btnNextt').onclick = function() {
    c.nextMonth();
  };
  getId('btnPrevv').onclick = function() {
    c.previousMonth();
  };
}

// Get element by id
function getId(id) {
  return document.getElementById(id);
}