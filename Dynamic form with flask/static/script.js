$(document).ready(function(){
    var i = 1;
    $('#add').click(function(){
        i++;
        $('#dynamic_field').append('<tr id="row'+i+'"><td><input type="text" name="name[]" placeholder="Enter another Name" /></td><td><button type="button" name="remove" id="'+i+'" class="btn_remove">X</button></td></tr>');
    });

    $(document).on('click', '.btn_remove', function(){
        var button_id = $(this).attr("id");
        $('#row'+button_id+'').remove();
    });

    $('#services').change(function(){
        var selectedService = $(this).val();
        if(selectedService !== ''){
            // Enable the status dropdown
            $('#status').prop('disabled', false);

            // Populate the status dropdown based on the selected service
            if(selectedService === 'Registry Administration'){
                $('#status').html('<option value="Manual">Manual</option><option value="Digitized">Digitized</option>');
            } else if(selectedService === 'ICT User Support Services'){
                $('#status').html('<option value="Manual">Manual</option><option value="Digitized">Digitized</option>');
            }
            // Add other services here
            else {
                // If no specific options for the selected service, clear the dropdown
                $('#status').html('');
                $('#status').prop('disabled', true);
            }

            // Enable the timeline dropdown
            $('#timeline').prop('disabled', false);

            // Enable the on-boarded dropdown
            $('#on_boarded').prop('disabled', false);

            // Populate the on-boarded dropdown based on selected service
            if(selectedService === 'Registry Administration' || selectedService === 'ICT User Support Services'){
                $('#on_boarded').html('<option value="Yes">Yes</option><option value="No">No</option>');
            } else {
                $('#on_boarded').html('<option value="No">No</option>');
            }

            // Enable the legal instrument dropdown
            $('#legal_instrument').prop('disabled', false);

            // Enable the changes required dropdown
            $('#changes_required').prop('disabled', false);

            // Enable the services to enhance dropdown
            $('#services_to_enhance').prop('disabled', false);

            // Populate the services to enhance dropdown based on selected service
            $('#services_to_enhance').html('');
            if(selectedService === 'Registry Administration'){
                $('#services_to_enhance').append('<option value="Registry Administration">Registry Administration</option>');
            } else if(selectedService === 'ICT User Support Services'){
                $('#services_to_enhance').append('<option value="ICT User Support Services">ICT User Support Services</option>');
            }
            // Add other services here
            // else if(selectedService === 'Another Service'){
            //     $('#services_to_enhance').append('<option value="Another Service">Another Service</option>');
            // }
        } else {
            // If no service is selected, disable and clear the status, timeline, on-boarded, legal instrument, changes required, and services to enhance dropdowns
            $('#status').prop('disabled', true);
            $('#status').html('');
            $('#timeline').prop('disabled', true);
            $('#timeline').html('');
            $('#on_boarded').prop('disabled', true);
            $('#on_boarded').html('');
            $('#legal_instrument').prop('disabled', true);
            $('#legal_instrument').val('');
            $('#changes_required').prop('disabled', true);
            $('#changes_required').val('');
            $('#services_to_enhance').prop('disabled', true);
            $('#services_to_enhance').html('');
        }
    });

    // Handling the selection of legal instrument
    $('#legal_instrument').change(function(){
        var selectedInstrument = $(this).val();
        if(selectedInstrument === 'Others'){
            $('#other_instrument').prop('disabled', false);
            $('#other_instrument').show();
        } else {
            $('#other_instrument').prop('disabled', true);
            $('#other_instrument').hide();
            $('#other_instrument').val('');
        }
    });

    // Handling the selection of changes required
    $('#changes_required').change(function(){
        var changesRequired = $(this).val();
        if(changesRequired === 'Yes'){
            $('#change_details').prop('disabled', false);
            $('#change_details').show();
        } else {
            $('#change_details').prop('disabled', true);
            $('#change_details').hide();
            $('#change_details').val('');
        }
    });

    // Submit form data via AJAX
    $('form').submit(function(event){
        event.preventDefault(); // Prevent the form from submitting normally

        // Serialize form data
        var formData = $(this).serialize();

        // Submit form data via AJAX
        $.ajax({
            type: 'POST',
            url: '/submit',
            data: formData,
            success: function(response){
                // Display pop-up message
                alert(response.message);
                // Redirect to the home page
                window.location.href = "/";
            },
            error: function(error){
                // Display error message if AJAX request fails
                alert('Error: ' + error.responseText);
            }
        });
    });
});
