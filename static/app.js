$(document).ready(function() {


    $("#login").on("click", function() {
        
        event.preventDefault(); 
        $('#loginModal').modal('show');
       
    });



       
    });
    

$(document).on("click", ".edit", function() {
        
    event.preventDefault();

    console.log(`edit button working`);

    console.log($(this).data('id'));

    
    let _id = $(this).data('id');
    let title = $(this).data('title');
    let body = $(this).data('body');

    console.log(`title: ${title}`);
    console.log(`body: ${body}`);

    $('#editModaltitle').text(title);
    $('#editModalbody').text(body);

    $('#editModal').modal('show');
   
});


$(document).on("click", ".delete", function() {
        
    event.preventDefault();

    console.log(`delete button IS NOT working`);
    
    let postid = $(this).data('id');
    console.log(`postid app2:  ${postid}`);

    $.ajax({
        url: '/delete/' + postid,
        method: "POST"
      }).done(function(res) {
        location.reload(true);          
})
});