var generate_modal = function(modal_text){
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
  }
  else{
    $("#word_count").html(280 - parseInt(input)).css('color','#A9A9A9');
    $("#post_btn").prop("disabled",false);
  }
}

var updateTweets = function(tweets){
  $("#tweets").empty()
  console.log("Within udpate Tweets")
  $.each(tweets, function( index, value ){
    createNewTweet(value);
  });
}


var createNewTweet = function(tweetData){
  console.log("creating new tweets")
  var textArea = $('<textarea id="tweet-text-modal" rows="7" cols="70">');
  var checkBox = $('<div class="add_tweet"><input type="checkbox" name="add_tweet"></div>');
  textArea.append(tweetData);
  textArea.prepend('\n');
  var date = new Date();
  var time = date.toLocaleString();
  id = $("#screen_name").text();
  console.log("ID")
  console.log(id)
  textArea.prepend(id + ' ' + time);
  $("#tweets").prepend(textArea)
  $("#tweets").prepend(checkBox)
  $("#tweets").append('<br>')
};


$(document).on('change', '#post_text', function() {
  console.log("detected change");
  wordCount();
});

var saveTweet = function(message){
  $.ajax({
        type: "POST", url: "save_tweet", dataType : "json", contentType: "application/json; charset=utf-8",
    data : JSON.stringify({'message': message}),
        success: function(result){
          updateTweets(result['tweets'])
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

var post = function(message){
  $.ajax({
        type: "POST", url: "post", dataType : "json", contentType: "application/json; charset=utf-8",
    data : JSON.stringify({'message': message}),
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
            generate_modal("Error sending Tweet")
        }
    });
}

var run_auth = function(){
  $.ajax({
    type: "POST", url: "auth", 
    success: function(result){
        console.log(result);
        var w = window.open(result, "popupWindow", "width=600,height=600,scrollbars=yes");
        $(w.document).find('html').addClass('popup')
    },
    error: function(request, status, error){
        console.log("Error");
        console.log(request)
        console.log(status)
        console.log(error)
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

    $( ".tweet_btn" ).mouseout(function() {
      $(".tweet_btn").removeClass(".btn_active").removeClass(".btn_hover")
    });

    $( ".tweet_btn" ).mouseover(function() {
      $(".tweet_btn").addClass(".btn_hover")
    });

    $(".tweet_btn").click(function() {
      $(".tweet_btn").removeClass(".btn_hover").addClass(".btn_active")
    });

    $("#post_text").click(function() {
        var message = $("#post_text").val();
    });

    $("#post_text").on("input", function(){
      // Print entered value in a div box
      wordCount();
    });

    $(document).on('click',"#post_btn",function() {
      var message = $("#post_text").val();
      saveTweet(message)
      post(message)
      $("#post_text").val('');
      wordCount();
    });

    $(document).on('click',"#save_btn",function() {
      var message = $("#post_text").val();
      saveTweet(message)
      $("#post_text").val('');
      wordCount();
    });

    $("input[type='image']").click(function() {
      $("input[id='my_file']").focus().click();
      
    });

});
