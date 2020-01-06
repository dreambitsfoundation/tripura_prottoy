$("#show_password").on("mousedown", function() {
  $("#new_password_input").attr("type", "text");
});

$("#show_password").on("mouseup", function() {
  $("#new_password_input").attr("type", "password");
});

$("#change_password").submit(function(event) {
  event.preventDefault();
  var form = $(this);
  $(form).addClass("loading");
  var formdata = jsonArrayToObject($(this).serializeArray());
  $.post("auth/change_password", JSON.stringify(formdata))
    .done(function(data) {
      if (data.status) {
        $("#change_password").trigger("reset");
        $("body").toast({
          title: "Success",
          message: data.message,
          showProgress: "bottom",
          class: "success"
        });
      } else {
        $("body").toast({
          title: "Error",
          message: data.message,
          showProgress: "bottom",
          class: "error"
        });
      }
      $(form).removeClass("loading");
    })
    .fail(function(data) {
      $("body").toast({
        title: "Error",
        message: data.responseJSON.message,
        showProgress: "bottom",
        class: "error"
      });
      $(form).removeClass("loading");
    });
});
