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

// Show Only Selected Job on click
let count = 0;
$(".see-full-job").click(function () {
  let job_expand = $(".job-expand");
  job_expand.css("visibility", "visible");

  //check the count of click to avoid element duplication
  if (count == 0) {
    let job_title = $(this).parent().find("h1").text();
    let company_name = $(this).parent().find("h4").text();
    let company_contract_address = $(this).parent().find("h2").text();
    let job_salary = $(this).parent().find("h3").text();
    let job_description = $(this).parent().find("p").text();
    let posted_date = $(this).parent().find("h5").text();
    // capture job-listing-box element and append to job-expand

    $(this).parent().parent().parent().find(job_expand)
      .append(`<h1 class="job-title">${job_title}</h1>
      <h4 class="company_name">${company_name}</h4>
      <h4 class="contract-type-location">${company_contract_address}</h4>
      <h3 class="job-salary">${job_salary}</h3>
      <hr>
      <form class="save-job_form" action="{{url_for('profile', jobs=jobs, user=user)}}" method="POST">
      <button class="save_job"></button>
      <span class="tooltip-job">Save a Job</span>    
      </form>
      <p>${job_description}</p>
      <h4 class="post-date">${posted_date}</h4>
      `);

    count++;

    //check the count of click to avoid element duplication
  } else if (count > 0) {
    // save each job component and append job-expand element dynamically
    let job_title = $(this).parent().find("h1").text();
    let company_name = $(this).parent().find("h4").text();
    let company_contract_address = $(this).parent().find("h2").text();
    let job_salary = $(this).parent().find("h3").text();
    let job_description = $(this).parent().find("p").text();
    let posted_date = $(this).parent().find("h5").text();
    $(".job-expand").children().remove();
    $(this).parent().parent().parent().find(job_expand)
      .append(`<h1 class="job-title">${job_title}</h1>
    <h4 class="company_name">${company_name}</h4>
    <h4 class="contract-type-location">${company_contract_address}</h4>
    <h3 class="job-salary">${job_salary}</h3>
    <hr>
    <form class="save-job_form" action="{{url_for('profile', jobs=jobs, user=user)}}" method="POST">
    <button class="save_job"></button>
    <span class="tooltip-job">Save a Job</span>    
    </form>
    <p>${job_description}</p>
    <h4 class="post-date">${posted_date}</h4>
    `);
  }

  $(".save-job_form")
    .after()
    .mouseover(function () {
      $(".tooltip-job").css("visibility", "visible");
    });

  $(".save-job_form")
    .after()
    .mouseleave(function () {
      $(".tooltip-job").css("visibility", "hidden");
    });
});

// Job-listing pagination

let numOfItems = $(".whole-listing .job-listing-box").length;
let itemsLimit = 3;

// Hide items on large screen
$(".job-listing .job-listing-box:gt(" + (itemsLimit - 1) + ")").hide();

//Hide items on small screen < 900px

$(".job-listing-mobile .job-listing-box:gt(" + (itemsLimit - 1) + ")").hide();

let totalPages = Math.ceil(numOfItems / itemsLimit);

// Append first page and loop through total number of pages

$(".pagination").append(
  "<li class='active' id='current-page'><a href='javascript:void(0)'>" +
    1 +
    "</a></li>"
);

for (let i = 2; i <= totalPages; i++) {
  $(".pagination").append(
    "<li id='current-page'><a href='javascript:void(0)'>" + i + "</a></li>"
  );
}

$(".pagination").append(
  "<li class='next_page' class='waves-effect'><a href='javascript:void(0)'><i class='fas fa-chevron-right'></i></a></li>"
);

//check the current page and update pages title

let current_page_count = $(".pagination li.active").index();
$(".page-count").text(`Page ${current_page_count} of ${totalPages}`);

//Function to navigate to the next/previous page when users selects desired one
$(".pagination li#current-page").click(function () {
  if ($(this).hasClass("active")) {
    return false;
  } else {
    current_page = $(this).index();
    $(".pagination li").removeClass("active");
    $(this).addClass("active");
    $(".whole-listing .job-listing-box").hide();

    let allItems = itemsLimit * current_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".whole-listing .job-listing-box:eq(" + i + ")").show();
    }
  }

  let current_page_count = $(".pagination li.active").index();
  $(".page-count").text(`Page ${current_page_count} of ${totalPages}`);
});

// Function to navigate to the next page when users click on next page icon
$(".next_page").click(function () {
  let selected_page = $(".pagination li.active").index();
  if (selected_page === totalPages) {
    return false;
  } else {
    selected_page++;
    $(".pagination li").removeClass("active");
    $(".whole-listing .job-listing-box").hide();

    let allItems = itemsLimit * selected_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".whole-listing .job-listing-box:eq(" + i + ")").show();
    }

    $(".pagination li#current-page:eq(" + (selected_page - 1) + ")").addClass(
      "active"
    );
  }

  //check the current page and update pages title
  $(".page-count").text(`Page ${selected_page} of ${totalPages}`);
});

// Function to navigate to the previous page when users click on previous page icon
$(".prev-page").click(function () {
  let selected_page = $(".pagination li.active").index();
  if (selected_page === 1) {
    return false;
  } else {
    selected_page--;
    $(".pagination li").removeClass("active");
    $(".job-listing .job-listing-box").hide();

    let allItems = itemsLimit * selected_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".job-listing .job-listing-box:eq(" + i + ")").show();
    }

    $(".pagination li#current-page:eq(" + (selected_page - 1) + ")").addClass(
      "active"
    );
  }

  //check the current page and update pages title
  $(".page-count").text(`Page ${selected_page} of ${totalPages}`);
});
