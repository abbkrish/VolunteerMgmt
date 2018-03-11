function check_field_value(new_val) {
    if(new_val === true) {
            // #id_field_four should be actually the id of the HTML element
            // that surrounds everything you want to hide.  Since you did
            // not post your HTML I can't finish this part for you.
            $('#parents_signature_div').show();
        } else {
            $('#parents_signature_div').hide();
        }
    }



    // this is executed once when the page loads
    $(document).ready(function() {

        //need the conditions below if the page reloads after submitting and the minor box is checked
        if ($('#id_minor').is(":checked")){
            $('#parents_signature_div').show();
        }
        else{
            $('#parents_signature_div').hide();
        }


        // set things up so my function will be called when field_three changes
        $('#minor_div').change( function() {
            check_field_value($('#id_minor').is(":checked"));
        });

    });