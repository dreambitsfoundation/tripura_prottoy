function jsonArrayToObject(jsonArray) {
  var jsonValue = {};
  for (let i = 0; i < jsonArray.length; i++) {
    jsonValue[jsonArray[i]["name"]] = jsonArray[i]["value"];
  }
  return jsonValue;
}
$("#signup").submit(function(event) {
  event.preventDefault();
  var formdata = jsonArrayToObject($(this).serializeArray());
  $.post("auth/user_account/", JSON.stringify(formdata))
    .done(function(data) {
      if (data.status) {
        $("#signup").trigger("reset");
        alert("Account is successfully created. Please Sign In Now");
      } else {
        alert("Error: " + data.message);
      }
    })
    .fail(function(data) {
      if (data.responseJSON.message !== undefined) {
        $("#signup_error")
          .text(data.responseJSON.message)
          .show();
      } else {
        $("#signup_error")
          .text("Something went wrong! Check your internet connection.")
          .show();
      }
    });
});

$("#signin").submit(function(event) {
  event.preventDefault();
  var formdata = jsonArrayToObject($(this).serializeArray());
  $.post("auth/login/", JSON.stringify(formdata))
    .done(function(data) {
      if (data.status) {
        window.location.href = data.data[0]["redirect"];
      } else {
        alert("Error: " + data.message);
      }
    })
    .fail(function(data) {
      if (data.responseJSON.message !== undefined) {
        $("#login_error")
          .text(data.responseJSON.message)
          .show();
      } else {
        $("#login_error")
          .text("Something went wrong! Check your internet connection.")
          .show();
      }
    });
});
