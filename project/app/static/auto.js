$(document).ready(function() {
    var autocompleteSelected = false;
    
    $('#searchBtn').prop('disabled',true);

    $('#school_name').on('input', function() {
        var inputValue = $(this).val().trim();
        
        // This is checking to ensure that the input that the user puts in is not A) empty and B) spaces
        if (!autocompleteSelected && inputValue === '') {
            $('#searchBtn').prop('disabled', true)
        } else {
            $('#searchBtn').prop('disabled', false)
        }
    });

    $('#school_name').on('autocompleteselect', function(event, ui) {
        autocompleteSelected = true;
        $('#searchBtn').prop('disabled', false);
    });

    $('#search-function').submit(function(event) {
        var inputValue = $('#school_name').val().trim();
        if (inputValue === '' || inputValue === null) {
            event.preventDefault(); // Prevent form submission
        }
        if (!autocompleteSelected) {
            event.preventDefault();
        }
    });

    $('#autocompleteResults').hide();

    $('#school_name').click(function() {
        $(this).autocomplete('search', '')
        $('#autocompleteResults').show()
        $(this).attr('placeholder', 'Scroll or search 2097 schools');
    })

    $('#school_name').autocomplete({
        source: function(request, response) {
            $.getJSON('/autocomplete', { query: request.term }, function(data) {
                response(data); // Pass the response data to the autocomplete widget
            });
        },
        minLength: 0,
        select: function(event, ui) {
            $('#school_name').val(ui.item.value);
            $('#search-fucntion').submit();
        }
    });
});
