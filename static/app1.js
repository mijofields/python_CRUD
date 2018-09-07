$(document).ready(function() {


    $("#login").on("click", function() {
        
        event.preventDefault(); 
        $('#loginModal').modal('show');
       
    });



       
    });
    

$(document).on("click", ".edit", function() {
        
    event.preventDefault();
    let postid = $(this).data('id');
    console.log(`edit button working`);

    $.ajax({
        url: '/edit/' + postid,
        method: "GET"
      }).done(function(response) {
          
        console.log(response);
})

   
});

$(document).on("click", ".delete", function() {
        
    event.preventDefault();
    
    let postid = $(this).data('id');
    console.log(`postid app2:  ${postid}`);

    $.ajax({
        url: '/delete/' + postid,
        method: "POST"
      }).done(function(response) {
          
        location.reload(true);
})
});

