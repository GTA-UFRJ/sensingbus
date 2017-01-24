/*$('#visualization-search').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    create_post(this);
});


function create_post(form) {
    console.log("Create post works");
    form.$(":input").each(function(){
        var input = $(this);
        console.log(input.val());
    });
}*/

var frm = $('#visualization-search');
frm.submit(function () {
    console.log(frm);
    console.log(frm.serialize());
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            console.log(data);
        },
        error: function(data) {
            console.log("Something went wrong!");
        }
    });
    return false;
});