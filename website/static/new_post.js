function jsonArrayToObject(jsonArray){
    var jsonValue = {};
    for(let i = 0; i<jsonArray.length; i++){
        jsonValue[jsonArray[i]["name"]] = jsonArray[i]["value"];
    }
    return jsonValue;
}
$("#new_post").submit(function(event){
    event.preventDefault();
    var formdata = jsonArrayToObject($(this).serializeArray());
    $.post(
        "api/post/",
        JSON.stringify(formdata)
    ).done(function(data){
        if(data.status){
            $('#new_post').trigger("reset");
            alert(data.message);
        }else{
            alert("Error: " + data.message);
        }
    }).fail(function(data){
        console.log(data)
    })
})