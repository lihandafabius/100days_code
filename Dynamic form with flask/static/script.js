$(document).ready(function(){
    // Handling the selection of services
    $('input[name="services[]"]').change(function(){
        // Enable other inputs
        $('#status').prop('disabled', false);
        $('#timeline').prop('disabled', false); // Enable timeline dropdown
        $('#on_boarded').prop('disabled', false); // Enable on-boarded dropdown
        $('#legal_instrument').prop('disabled', false);
        $('#changes_required').prop('disabled', false);
        $('#services_to_enhance').prop('disabled', false);

        // Clear existing options in services_to_enhance
        $('#services_to_enhance').html('');

        // Populate timeline dropdown based on selected services
        var selectedServices = [];
        $('input[name="services[]"]:checked').each(function(){
            selectedServices.push($(this).val());
        });

        populateTimelineDropdown(selectedServices);
    });

    // Function to populate timeline dropdown based on selected services
    function populateTimelineDropdown(selectedServices) {
        $('#timeline').html('<option value="" disabled selected>Select timeline</option>');
        // Loop through selected services and populate timeline dropdown accordingly
        selectedServices.forEach(function(service) {
            if (service === 'Registry Administration') {
                $('#timeline').append('<option value="Y1-2023/24">Y1-2023/24</option>');
                $('#timeline').append('<option value="Y2-2024/25">Y2-2024/25</option>');
                $('#timeline').append('<option value="Y3-2025/26">Y3-2025/26</option>');
                $('#timeline').append('<option value="Y4-2026/27">Y4-2026/27</option>');
            } else if (service === 'ICT User Support Services') {
                $('#timeline').append('<option value="Y1-2024/25">Y1-2024/25</option>');
                $('#timeline').append('<option value="Y2-2025/26">Y2-2025/26</option>');
                $('#timeline').append('<option value="Y3-2026/27">Y3-2026/27</option>');
                $('#timeline').append('<option value="Y4-2027/28">Y4-2027/28</option>');
            }
            // Add more conditions for other services if needed
        });
    }

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

    // Handling the selection of on-boarded status
    $('#on_boarded').change(function(){
        var onBoardedStatus = $(this).val();
        // Example logic: Alert the selected status
        alert('On-boarded status: ' + onBoardedStatus);
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
