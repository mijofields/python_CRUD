$(document).ready(function() {


    $("#login").on("click", function() {
        
        event.preventDefault(); 
        $('#loginModal').modal('show');
       
    });
       
    });
    

    $(document).on("click", ".edit", function() {
        
        event.preventDefault();
        let postid = $(this).data('id');

        $.ajax({
            url: '/edit/' + postid,
            method: "GET",
            success:function(response){ document.write(response)}
          })
    //success returns control to Flask, allowing for the route to work
       
    });


$(document).on("click", ".delete", function() {
        
    event.preventDefault();
    
    let postid = $(this).data('id');

    $.ajax({
        url: '/delete/' + postid,
        method: "POST",
        success:function(response){ document.write(response)}
      })
});