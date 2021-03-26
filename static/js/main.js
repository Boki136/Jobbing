// Materialize initialization
$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });
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
