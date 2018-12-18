$(function() {
$(document).ready(function () {
    $('#option-group-signup').multiselect();
});



$('#filter_submit').click(function() {
    var val = $('#age').val()
    var gender = $('#gender').val()
    $.ajax({
        type: "POST",
        url: 'filtered/',
        data: {
            'val': val,
            "gender": gender,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),

        },
        success: getFiltered,
        error: function() {
            alert("error")
        }
    });
});


function getFiltered(response) {
    $("#tbody_id").empty()
    var Json = JSON.parse(response)
    textlist = ""
    for (var i = 0; i < Json.length; i++) {
        textlist += "<tr> <td class='usernames'>" + Json[i][0] + '</td> <td>' + Json[i][1] + "</td> <td> <button style='width:100px' class='match' id =" + i + " value =" + Json[i][0] + "> Match </button> </td></tr>"
    }
    $("#tbody_id").html(textlist)

}




$("body").on('click', ".clickable-row", function() {
    window.location = $(this).data("href");

});
