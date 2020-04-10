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

// This is the wordcount function for tweets in the thread
var wordCount2 = function (i) {
  var input = $(".tweet-text-modal."+String(i)).val().length;

  if (input > 280) {
    $(".word_count_tweets."+i).html(280 - parseInt(input)).css('color', 'red');
    $("#post_btn").prop("disabled", true);
  } else {
    $(".word_count_tweets."+i).html(280 - parseInt(input)).css('color', '#A9A9A9');
    if (screen_name != "Demo_User") {
      $("#post_btn").prop("disabled", false);
    }
  }
}


var tweets_array = []

var addTweet = function(message) {
  tweets_array.push(message)
  createNewTweet(message)
}


var deleteTweet = function(i) {
  console.log('made it' + $('#tweets').get(0))
  $("#tweet_" + String(i)).remove()
  delete tweets_array[i]
}

// var updateTweets = function(tweets){
//   $("#tweets").empty()
//   console.log("Within update Tweets")
//   x = document.getElementsByClassName('x_btn')
//   i = 0
//   $.each(tweets, function( index, value ){
//     createNewTweet(value, i);
//     //$("#tweets").prepend(checkBox)
//   })
  
// }

i = 0 // This is to keep track of each tweet index

var createNewTweet = function(tweetData){
  var textArea = $('<textarea class="tweet-text-modal '+i+'" rows="7" cols="70" oninput="wordCount2('+i +')">');
  var button = $('<button class="x_btn '+i+'" onClick="deleteTweet(' + i +')"><i class="fa fa-close"></button></div>');
  var wordcount = $('<div class="word_count_tweets '+i+'">'+ String(280-tweetData.length) +'</div>');

  textArea.append(tweetData);

  $("#tweets").prepend(button)
  $("#tweets").prepend(textArea)
  $("#tweets").prepend(wordcount)

  $('.'+i).wrapAll('<div id="tweet_'+ i + '"></div>') // Wrap in a div so it can be deleted
  
  scrollDown()
  i++
};

// $(document).on('change', '#post_text', function() {
//   console.log("detected change");
//   wordCount();
// });

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

var scrollDown = function() {
  adds = document.getElementById('add-ons')
  adds.scrollTop = adds.scrollHeight
  console.log(adds.scrollTop)
}

$(document).mousemove(function(event){
  //console.log("Window reference");
  //console.log(window.location.href)
});

$(document).ready(function(){
  

    // updateTweets(tweets)

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

    // $("#post_text").click(function() {
    //     var message = $("#post_text").val();
    // });

    // $(document).on('change', '.tweet_text_modal', function() {
    //   text_modals = document.getElementsByClassName('tweet_text_modal')
    //   for( i =0; i < text_modals)
    // })

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
        //updateTweets(tweets);
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
