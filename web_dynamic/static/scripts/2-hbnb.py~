$(document).read(function() {
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
});
