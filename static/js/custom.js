// Function to clear shipping address form 

$(document).ready(function(){ 

    $("#clear-form").click(function() {

        $("#shipping-form").each(function(){
            $(this).find('input').val("");
        })

    })

})