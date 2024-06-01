$(document).ready(function() {
    let selectedAmenities = {};

    $('input[type="checkbox"]').change(function() {
	let amenityId = $(this).data('id');
	let amenityName = $(this).data('name');

	if ($(this).is(':checked')) {
	    selectedAmenities[amenityId] = amenityName;
	}
	else {
	    delete selectedAmenity[amenityId];
	}

	let amenitiesList = Object.values(selectedAmenities).join(', ');
	$('.amenities h4').text(amenitiesList);
    });

    $.ajax({
	type: 'GET',
	url: 'https://google.com',
	success: function(data, textStatus, xhr) {
	    console.log(xhr.status)
	}
    })
});
