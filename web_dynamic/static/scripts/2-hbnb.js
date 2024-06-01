$(document).ready(function() {
  let checkedAmenities = {};
  $(document).on('change', "input[type='checkbox']", function() {
    if (this.checked) {
      checkedAmenities[$(this).parent().data('id')] = $(this).parent().data('name');
    } else {
      delete checkedAmenities[$(this).parent().data('id')];
    }
    let lst = Object.values(checkedAmenities);
    if (lst.length > 0) {
      $("div.amenities > h4").text(Object.values(checkedAmenities).join(', '));
    } else {
      $("div.amenities > h4").html("&nbsp;");
    }
  });

  $.get('http://0.0.0.0:5001/api/v1/status/', function(data, textStatus) {
    if (textStatus === 'success') {
      if (data.status === 'OK') {
        $('#api_status').addClass('available');
      } else {
        $('#api_status').removeClass('available');
      }
    }
  });
});
