$(document).ready(function() {


    $("#login").on("click", function() {
        
        event.preventDefault(); 
        $('#loginModal').modal('show');
       
       
        // $.ajax({
        //     url: "/scrape",
        //     method: "GET"
        //   }).done(function(res) {

        //     location.reload(true);

        //    });  
    })

});