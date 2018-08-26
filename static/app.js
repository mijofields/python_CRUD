$(document).ready(function() {


    $("#login").on("click", function() {
        console.log(`weird log in script 1`);
        event.preventDefault();
        console.log(`weird log in script 2`);
        $('#loginModal').modal('show');
       
       
        // $.ajax({
        //     url: "/scrape",
        //     method: "GET"
        //   }).done(function(res) {

        //     location.reload(true);

        //    });  
    })

});