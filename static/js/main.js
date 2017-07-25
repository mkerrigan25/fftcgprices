$(document).ready(function () {
    //your code here
  var $rows = $('#table tr').not(':first');
  $('#search').keyup(function() {

      var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
          reg = RegExp(val, 'i'),
          text;

      $rows.show().filter(function() {
          text = $(this).text().replace(/\s+/g, ' ');
          return !reg.test(text);
      }).hide();
  });
});