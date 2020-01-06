function approvePost(id){
    var decission = confirm("Are you sure you want to approve this post?");
    if(decission){
        $.ajax({
          method: "PUT",
          url: "api/post/",
          data: JSON.stringify({"id": id, "publish": "True"})
        })
          .done(function( data ) {
            console.log(data);
            if(data.status){
                location.reload(true);
            }
        });
    }
}

function rejectPost(id){
    var decission = confirm("Are you sure you want to reject this post?");
    if(decission){
        $.ajax({
          method: "PUT",
          url: "api/post/",
          data: JSON.stringify({"id": id, "publish": "False"})
        })
          .done(function( data ) {
            console.log(data);
            if(data.status){
                location.reload(true);
            }
        });
    }
}