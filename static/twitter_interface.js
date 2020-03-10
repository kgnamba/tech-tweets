$(document).ready(function(){
    console.log("loaded");

    $("#post_text").click(function() {
        console.log("this works in twitter_interface");
        $("#post_text").val() = '';
    });

    $("#twitter_btn").click(function(){
        console.log("Called from twitter_interface");
    });


});

// //<a id="twitter_btn" class="twitter-share-button" data-size="large" data-lang="en">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>