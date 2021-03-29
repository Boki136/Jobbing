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


// Register form option selection funcionality

let register_employer = $(".register-employer-form");
let register_jobseeker = $(".register-jobseeker-form");

$(".employer-register").click(function() {
    register_employer.css("display", "block")
    register_jobseeker.css("display", "none")
})

$(".jobseeker-register").click(function() {
    register_employer.css("display", "none")
    register_jobseeker.css("display", "block")
})