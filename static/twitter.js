var generate_modal = function(modal_text){
  // Creates the Area to see tweet thread
  $(".modal-header").empty();
  $(".modal-header").append('<div class="modal-text">' + modal_text + '</div>');
  $(".modal-header").append('<button type="button" class="close" data-dismiss="modal">&times;</button>');
  $("#mymodal").modal({show:true});
}

var wordCount = function(){
  var input = $("#post_text").val().length;

  if(input > 280){
    $("#word_count").html(280 - parseInt(input)).css('color','red');
    $("#post_btn").prop("disabled",true);
    $("#post_btn").addClass("btn_disable");
  }
  else{
    $("#word_count").html(280 - parseInt(input)).css('color','#A9A9A9');
    if (screen_name != "Demo_User") {
      $("#post_btn").prop("disabled", false);
      $("#post_btn").removeClass("btn_disable");
    }
  }
}

var wordCount2 = function () {
  var input = $("#tweet-text-modal").val().length;
  console.log('wordcount2 called')

  if (input > 280) {
    $(".word_count_tweets").html(280 - parseInt(input)).css('color', 'red');
    $("#post_btn").prop("disabled", true);
  } else {
    $("#word_count").html(280 - parseInt(input)).css('color', '#A9A9A9');
    if (screen_name != "Demo_User") {
      $("#post_btn").prop("disabled", false);
    }
  }
}


var tweets_array = []

var addTweet = function(message) {
  tweets_array.push(message)
  createNewTweet(message)
  console.log(tweets_array)
}


var deleteTweet = function() {

}

var updateTweets = function(tweets){
  $("#tweets").empty()
  console.log("Within update Tweets")
  $.each(tweets, function( index, value ){
    createNewTweet(value);
    //$("#tweets").prepend(checkBox)
  });
}


var createNewTweet = function(tweetData){
  console.log("creating new tweets")
  var textArea = $('<textarea id="tweet-text-modal" rows="7" cols="70" onchange="wordCount2()">');
  var checkBox = $('<button id="x_btn"><i class="fa fa-close"></button>');
  var wordcount = $('<div class="word_count_tweets">280</div>');
  textArea.append(tweetData);
  $("#tweets").prepend(textArea)
  $("#tweets").prepend(checkBox)
  $("#tweets").prepend(wordcount)
};

$(document).on('change', '#post_text', function() {
  console.log("detected change");
  wordCount();
});

var post = function(tweets){
  $.ajax({
        type: "POST", url: "post", dataType : "json", contentType: "application/json; charset=utf-8",
        data : JSON.stringify({'tweets': tweets}), // send to server and post to twitter
        success: function(result){
          id = result['screen_name'];
          url = 'https://twitter.com/#!/' + id;
          window.open(url);
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
            console.log(tweets)
            generate_modal("Error sending Tweet")
        }
    });
}

$(document).mousemove(function(event){
  //console.log("Window reference");
  //console.log(window.location.href)
});

$(document).ready(function(){
  

    updateTweets(tweets)

    $("#screen_name").empty();
    $("#screen_name").append(screen_name)

    if (screen_name== "Demo_User") {
      // Disable post button if in Demo Mode
      $("#post_btn").prop("disabled", true);
      $("#post_btn").addClass("btn_disable")
    }

    $( ".tweet_btn" ).mouseout(function() {
      $(".tweet_btn").removeClass("btn_hover")
    });

    $( "#post_btn" ).mouseover(function() {
      if(document.getElementById("post_btn").disabled != true) {
        $("#post_btn").addClass("btn_hover")
      }
    });

    $("#add_btn").mouseover(function() {
      $("#add_btn").addClass("btn_hover")
    })

    $(".tweet_btn").click(function() {
      if (document.getElementById("post_btn").disabled != true) {
        $(".tweet_btn").removeClass("btn_hover")
      }
    });

    $("#post_text").click(function() {
        var message = $("#post_text").val();
    });

    $("#post_text").on("input", function(){
      // Print entered value in a div box
      wordCount();
    });

    $(document).on('click',"#post_btn", function() {
      var message = $("#post_text").val();
      if (document.getElementById("post_btn").disabled != true) {
        if (message.length > 0) {
          // this condition is so that no extra tweet posted if 
          // user has textbox selected
          addTweet(message);
        }
        console.log(tweets_array)
        post(tweets_array)
        $("#post_text").val('');
        tweets_array = []
        updateTweets(tweets);
        wordCount();
      }
      
    });

    $(document).on('click',"#add_btn",function() {
      var message = $("#post_text").val();
      addTweet(message)
      $("#post_text").val('');
      wordCount();
      console.log("add buttton clicked")
    });

    $("input[type='image']").click(function() {
      $("input[id='my_file']").focus().click();
      
    });

});
