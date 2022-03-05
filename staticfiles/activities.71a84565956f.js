$.get( "api/post/", function( data ) {
    console.log(data.data);
  if(data.data.length){
    $("#no_post_alert").hide();
    var postlist = "";
    for(let i = 0; i< data.data.length; i++){
        var labelColor = "";
        var label = "";
        if(data.data[i]['pending']){
            labelColor = "orange";
            label = "Under Review";
        }else{
            if(data.data[i]['approved']){
                labelColor = "green";
                label = "Published";
            }
            if(data.data[i]['rejected']){
                labelColor = "red";
                label = "Rejected";
            }
        }
        postlist += '<div class="ui segment">' +
        '<a style="font-size: large" href="/postView?id=' + data.data[i]['id'] + '">' + data.data[i]['title'] + '</a><br>' +
        '<small>' + data.data[i]['organisation'] + '</small>' +
        '&nbsp;<div class="ui label mini ' + labelColor  + '">' + label +
        '</div><div class="ui message">' +
        data.data[i]['body'] + '</div><small><b>Comments</b>: ' + data.data[i]['comments'].length + '&nbsp;&nbsp;&nbsp;<b>Posted On</b>: ' + data.data[i]['posted_on'] + '</small></div>';
    }
    $("#post_content").html(postlist);
  }else{
    $("#no_post_alert").show();
  }
});

$.get( "api/comment/", function( data ) {
  if(data.data.length){
    $("#no_comment_alert").hide();
    var commentlist = "";
    for(let i = 0; i< data.data.length; i++){
        commentlist += '<div class="ui segment">' +
        '<a style="font-size: large" href="/postView?id=' + data.data[i]['post_id'] + '#postcomment' + data.data[i]['id'] + '">#POST' + data.data[i]['post_id'] + '</a><br>' +
        '<small>' + data.data[i]['last_updated'] + '</small><div class="ui divider"></div>' + data.data[i]['text'] + '</div>';
    }
    $("#comment_content").html(commentlist);
  }else{
    $("#no_comment_alert").show();
  }
});