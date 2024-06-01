$(function () {
    $.ajax({
        type: 'GET',
        url: 'https://swapi-api.alx-tools.com/api/films/?format=json',
        success: function(names) {
            $.each(names.results, function(i, nm) {
                $('#list_movies').append('<li>' + nm.title + '</li>')
            });
        }
    });
});
