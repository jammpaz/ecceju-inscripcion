(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.carousel').carousel();
    $('.parallax').parallax();
    $('.dropdown-button').dropdown();
    $('.datepicker').pickadate({
      selectYears: 15,
      format: 'yyyy-mm-dd',
      today: 'hoy',
      monthsFull: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"]
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space
