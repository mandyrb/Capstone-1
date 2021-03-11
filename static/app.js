// A few front-end interactive components for Paragraph A Day

$(document).ready(function() {
    //Hide example paragraph content on home page
    $(".hide-me").hide();

    //Make sure text area for paragraph submission shows remaining characters allowed
    let currentLength = $('textarea').val().length;
    $('#char_count').text(`characters remaining: ${500 - currentLength}`);
});

//Show example paragraph content on home page when title is clicked
$("button").click(function(){

    if ($(this).next().is(":hidden")){
        $(this).next().show();
    }
    else {
        $(this).next().hide();
    }
})

//Show character countdown as user inputs paragraph content
$('textarea').on("input", function(){

    let currentLength = $(this).val().length;
    $('#char_count').text(`characters remaining: ${500 - currentLength}`);

});




