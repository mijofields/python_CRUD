$(document).ready(function() {


    $("#login").on("click", function() {
        
        event.preventDefault(); 
        $('#loginModal').modal('show');
       
    });

    

});

$(document).on("click", ".edit", function() {
        
    event.preventDefault(); 
    console.log(`edit button`);
    $('#editModal').modal('show');
   
});