// Materialize initialization
$(document).ready(function () {
  $(".sidenav").sidenav({ edge: "right" });
  $("select").formSelect();
});

// FAQ Dropdown Funcionality

$(".question-dropdown").click(function () {
  let paragraphState = $(this).children("p").css("display");
  if (paragraphState === "none") {
    $(this).children("i").css({ transform: "rotateZ(45deg)" });
  } else {
    $(this).children("i").css({ transform: "rotateZ(0deg)" });
  }

  $(this).children("p").toggle();
});

// Append Flash Message after registration selection and fade out after 3 sec

$(".register-selector").append($(".flash-message-container"));
$(".login-form").prepend($(".flash-message-container"));
$(".flash-message-container").delay(3000).fadeOut();

// Enable editing user details fields on click

$(".edit-user-info").click(function () {
  $(this).next().next().children(".edit").prop("disabled", false);
  $(this).next().next().children("button").css("display", "block");
  $(this).css("display", "none");
  $(this).next().css("display", "block");
});

$(".close-user-info").click(function () {
  $(this).next().children("input").prop("disabled", true);
  $(this).next().children("button").css("display", "none");
  $(this).css("display", "none");
  $(this).prev().css("display", "block");
});

// Show limited number of text for the job description

$(".job-description").each(function (i) {
  len = $(this).text().length;
  if (len > 250) {
    $(this).text($(this).text().substr(0, 250) + "...");
  }
});

// Show Only Selected Job on click
let count = 0;
$(".see-full-job").click(function () {
  let job_expand = $(".job-expand");
  job_expand.css("visibility", "visible");
  //check the count of click to avoid element duplication
  if (count == 0) {
    let job_title = $(this).parent().find("h1").text();
    let job_location = $(this).parent().find("h2").text();
    let job_salary = $(this).parent().find("h3").text();
    let job_description = $(this).parent().find("p").text();
    let posted_date = $(this).parent().find("h4").text();
    // capture job-listing-box element and append to job-expand

    $(this).parent().parent().parent().find(job_expand)
      .append(`<h1 class="job-title">${job_title}</h1>
      <h2 class="contract-type-location">${job_location}</h2>
      <h3 class="job-salary">${job_salary}</h3>
      <hr>
      <form class="save-job_form" action="{{url_for('find_job')}}" method="POST">
      <button class="save_job">Save a Job</button>
    </form>
      <p>${job_description}</p>
      <h4 class="post-date">${posted_date}</h4>
      `);

    count++;

    //check the count of click to avoid element duplication
  } else if (count > 0) {
    let job_title = $(this).parent().find("h1").text();
    let job_location = $(this).parent().find("h2").text();
    let job_salary = $(this).parent().find("h3").text();
    let job_description = $(this).parent().find("p").text();
    let posted_date = $(this).parent().find("h4").text();
    $(".job-expand").children().remove();
    $(this).parent().parent().parent().find(job_expand)
      .append(`<h1 class="job-title">${job_title}</h1>
    <h2 class="contract-type-location">${job_location}</h2>
    <h3 class="job-salary">${job_salary}</h3>
    <hr>
    <form class="save-job_form" action="{{url_for('find_job')}}" method="POST">
    <button class="save_job">Save a Job</button>
  </form>
    <p class="job-description">${job_description}</p>
    <h4 class="post-date">${posted_date}</h4>
    `);
  }
});
