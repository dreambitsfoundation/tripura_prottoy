function jsonArrayToObject(jsonArray){
    var jsonValue = {};
    for(let i = 0; i<jsonArray.length; i++){
        jsonValue[jsonArray[i]["name"]] = jsonArray[i]["value"];
    }
    return jsonValue;
}
$(".comment_form").submit(function(event){
    event.preventDefault();
    var formdata = jsonArrayToObject($(this).serializeArray());
    $.post(
        "api/comment/",
        JSON.stringify(formdata)
    ).done(function(data){
        if(data.status){
            location.reload(true);
        }else{
            $(this).trigger("reset");
            alert("Error: " + data.message);
        }
    }).fail(function(data){
        console.log(data)
    })
})