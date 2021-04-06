// Materialize initialization
$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });
    $("select").formSelect();
});



// FAQ Dropdown Funcionality

$(".question-dropdown").click(function () {

    let paragraphState = $(this).children("p").css("display");
    if (paragraphState === "none") {
        $(this).children("i").css({ transform: "rotateZ(45deg)" })
    } else {
        $(this).children("i").css({ transform: "rotateZ(0deg)" })
    }

    $(this).children("p").toggle()

});

// Append Flash Message after registration selection and fade out after 3 sec

$(".register-selector").append($(".flash-message-container"));
$(".login-form").prepend($(".flash-message-container"));
$(".flash-message-container").delay(3000).fadeOut();

// Enable editing user details fields on click

$(".edit-user-info").click(function() {
    $(this).next().next().children(".edit").prop('disabled', false);
    $(this).next().next().children("button").css("display", "block");
    $(this).css("display", "none");
    $(this).next().css("display", "block");
});

$(".close-user-info").click(function() {
    $(this).next().children("input").prop('disabled', true);
    $(this).next().children("button").css("display", "none");
    $(this).css("display", "none");
    $(this).prev().css("display", "block");
});