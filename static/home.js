
var run_auth = function(){
    $.ajax({
      type: "POST", url: "auth", 
      success: function(result){
          console.log(result);
          var w = window.location = result
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request)
          console.log(status)
          console.log(error)
      }
    });
  }

$(document).ready(function(){

    $("#log-in-btn").click(function(){
      run_auth()
    });

});
