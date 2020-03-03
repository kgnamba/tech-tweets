var examples = ["What can fossil plankton tell us about the last ice age?",
                "How do we know how many hurricanes struck the NYC area in the 12th century?",
                "How can massive corals give us climate information from the 1500s?",
                "Causal Inference: What is it about?",
                "Confounding Bias and how to control for it",
                "Causal Inference in the Big data era",
                "Why are bottlenecks in global ocean circulation important?",
                "What role could the Indian Ocean play in future climate change?",
                "How do changes in small straits and larger oceans affect one another?",
                "What is memory safety? and why it is still an issue regardless 30 years of research?",
                "What is a code re-use attack in computer programs?",
                "How to design/build a secure computer?",
                "people frequently misinterpret the cone of uncertainty for understanding hurricane risk."];

var hook_types = {
    'time-peg': {
        'text': 'time peg -  why is this relevant right now?',
        'example-tweet': '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Everyone&#39;s talking about impeachment and Clinton &amp; Johnson as the only presidents ever impeached. But most people don&#39;t know WHY Johnson was impeached.<br><br>So let me tell you the story about how not impeaching a racist president is a BIG reason why white supremacy lingers in America</p>&mdash; michaelharriot (@michaelharriot) <a href="https://twitter.com/michaelharriot/status/1204924987100073984?ref_src=twsrc%5Etfw">December 12, 2019</a></blockquote>'
    },
    'narrative-peg': {
        'text': 'narrative peg - what inspired you to explain this?',
        'example-tweet': '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">My university just announced that it’s dumping Blackboard, and there was much rejoicing. Why is Blackboard universally reviled? There’s a standard story of why &quot;enterprise software&quot; sucks. If you’ll bear with me, I think this is best appreciated by talking about… baby clothes!</p>&mdash; Arvind Narayanan (@random_walker) <a href="https://twitter.com/random_walker/status/1182635589604171776?ref_src=twsrc%5Etfw">October 11, 2019</a></blockquote>'
    },
    'correction': {
        'text': 'correction - are you responding to something you think people are misinterpreting?',
        'example-tweet': '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">1. All this talk about opposition research tonight is driving me nuts because so many people are getting it wrong (not Kyle). This is an area I know well, I got my training as a oppo researcher many years ago, I have also commissioned, disseminated, and received a ton of research <a href="https://t.co/f07SUEUV9Q">https://t.co/f07SUEUV9Q</a></p>&mdash; Yashar Ali 🐘 (@yashar) <a href="https://twitter.com/yashar/status/1093381319428530176?ref_src=twsrc%5Etfw">February 7, 2019</a></blockquote>'
    },
    'mystery': {
        'text': 'question or mystery - is there something unusual or unexpected that you will explain?',
        'example-tweet': '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Geeky thread warning. Or, if you’re like me, a cool bit of 20th Century urban archaeology. Check out this shop in Kingston. What’s unusual about it (aside from its no-doubt-excellent nails service)? <a href="https://t.co/MT3G9Yii9Z">pic.twitter.com/MT3G9Yii9Z</a></p>&mdash; Mark Wallace (@wallaceme) <a href="https://twitter.com/wallaceme/status/1110836282480082944?ref_src=twsrc%5Etfw">March 27, 2019</a></blockquote>'
    }                   
};

var panel_tabs = {
    'types': {'text': 'Hook types'},
    'newsapi-bert': {'text': 'Related news'},
    'newsapi-goog': {'text': 'Google news'},
    'tweets': {'text': 'Related tweets'}
};


function get_questions() {
    console.log('getting questions...');
    var value = $('.first-tweet-input').val();
    $('.posed-questions').empty();
    $.post("/api/get_noun_phrases", {'text': value}, function(resp) {
        console.log('response:', resp);
        $.each(resp.questions, function(i, item) {
            $('.posed-questions').append($('<p>').text(item));
        })
    })
}

$(document).ready(function(){
    $('.spinner-border').hide();
    $('.panel').hide();

    $(".get-tweets").click( function() {
        console.log('get-tweets button');
        var value = $('.keywords-input').val();
        $('.statuses').empty();
        $.post("/api/get_tweets", {'text': value}, function(resp) {
            console.log("response:", resp);
            if (resp.statuses.length === 0) {
                $('.statuses').append('No tweets with at least 100 likes found. Only searches the past few days. Try less keywords.')
            } else {
                $.each(resp.statuses, function(i, item) {
                    $('.statuses').append(item.html);
                });
            }
            
        });
    });

    $(".get-questions").click( function() {
        get_questions();
    });

    $.each(examples, function (i, val) {
        var text = $("<small/>").text(val);
        var ex = $("<a/>")
            .addClass('dropdown-item')
            .attr('id', i)
            .append(text);
        $('.dropdown-menu').append(ex);
    });

    $(".dropdown-item").click(function() {
        var id = $(this).attr('id');
        var text = examples[id];
        $('.first-tweet-input').val(text);
    });

    $.each(hook_types, function(key, val) {
        var item = $("<li />").append(val.text + ' ');
        
        var link = $("<a />")
            .attr('data-toggle', 'collapse')
            .addClass('collapsed')
            .attr('href', '#'+key)
            .attr('role', 'button')
            .attr('aria-expanded', 'false')
            .text('see example');
        item.append(link);
        var ex = $("<div />")
            .addClass('ex')
            .attr('id', key)
            .append(val['example-tweet']);
        $('.types-list').append(item).append(ex);
    });

    $.each(panel_tabs, function(key, val) {
        var item = $('<li />')
            .addClass('breadcrumb-item')
            .text(val.text)
            .click( function() {
                $('.breadcrumb-item').removeClass('active');
                $('.panel').hide();
                $('.'+key).show();
                $(this).addClass('active');
            });
        $('.breadcrumb').append(item);
    });

    $('.auth').click( function() {
        $.post('auth', function(resp) {
            console.log('auth resp:', resp);
            var w = window.location = resp;
        });
    });

    $(".get-help").click(function(){
        console.log('get-bert-help');
        value = $('.first-tweet-input').val();
        $('.query-text').empty().text('Query: ' + value);
        $('.news-results').empty();
        $('.spinner-border').show();
        $.post("/api/get_news", {'text': value}, function(resp) {
            console.log("response:", resp);
            $('.spinner-border').hide();
            $.each(resp.articles, function(i, item) {
                var card = $("<div/>"); //.addClass('card');
                var art = $("<div/>"); //.addClass('article');
                art.append($("<p/>").addClass('article').text(item.title));
                // art.append($("<p/>").addClass('small').text(item.firstsent));
                art.append($("<footer/>")
                    .addClass('blockquote-footer')
                    .text((item.sim*100).toFixed(0).toString() + "% related, from " + item.source.name + "; " + item.publishedAt));
                card.append(art);
                $('.news-results').append(card);
            });
        });
    });

    $(".get-goog-help").click(function(){
        console.log('get-goog-help');
        value = $('.keywords-input').val();
        $('.goog-query-text').empty().text('Query: ' + value);
        $('.goognews-results').empty();
        $('.spinner-border').show();
        $.post("/api/get_goog_news", {'text': value, 'tbs': "qdr:m"}, function(resp) {
            console.log("response:", resp);
            $('.spinner-border').hide();
            $.each(resp.news_results, function(i, item) {
                var card = $("<div/>"); 
                var art = $("<div/>"); 
                art.append($("<p/>").addClass('article').text(item.title));
                art.append($("<footer/>")
                    .addClass('blockquote-footer')
                    .text("from " + item.source + "; " + item.date));
                card.append(art);
                $('.goognews-results').append(card);
            });
        });
    });

});