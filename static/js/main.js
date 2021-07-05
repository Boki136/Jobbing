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

// search job by category trigger

$(".fa-angle-double-right").click(function () {
  $(this).prev().click();
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
      <h3 class="job-salary-expand">${job_salary}</h3>
      <p class="full-job-description">${job_description}</p>
      <h4 class="post-date">${posted_date}</h4>
      <i class="fas fa-times close-job"></i>
      `);

    $(".close-job").click(function () {
      $(this).parent().css("visibility", "hidden");
    });

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
    <h3 class="job-salary-expand">${job_salary}</h3>
    <p class="full-job-description">${job_description}</p>
    <h4 class="post-date">${posted_date}</h4>
    <i class="fas fa-times close-job"></i>
    `);

    $(".close-job").click(function () {
      $(this).parent().css("visibility", "hidden");
    });
  }
});

// Job-listing pagination

let numOfItems = $(".whole-listing .job-box").length;
let itemsLimit = 3;

// Hide items on large screen
$(".whole-listing .job-box:gt(" + (itemsLimit - 1) + ")").hide();

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
    $(".whole-listing .job-box").hide();

    let allItems = itemsLimit * current_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".whole-listing .job-box:eq(" + i + ")").show();
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
    $(".whole-listing .job-box").hide();

    let allItems = itemsLimit * selected_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".whole-listing .job-box:eq(" + i + ")").show();
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
    $(".whole-listing .job-box").hide();

    let allItems = itemsLimit * selected_page;

    for (let i = allItems - itemsLimit; i < allItems; i++) {
      $(".whole-listing .job-box:eq(" + i + ")").show();
    }

    $(".pagination li#current-page:eq(" + (selected_page - 1) + ")").addClass(
      "active"
    );
  }

  //check the current page and update number of pages title
  $(".page-count").text(`Page ${selected_page} of ${totalPages}`);
});

//transitions

$(".saved-job-box").mouseover(function () {
  $(this).find("img").css({ position: "absolute", left: "10px" });
});

$(".saved-job-box").mouseleave(function () {
  $(this).find("img").css({ position: "absolute", left: "0" });
});

// hide saved-jobs if no jobs displayed

saved_jobs_count = $(".saved-jobs-total").text();

if (saved_jobs_count == "0") {
  $(".saved-page-count, .saved-jobs-pages").remove();
}

//Show Company Location On Google Maps

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("company-location"), {
    center: { lat: 53.3450082, lng: -6.272111 },
    zoom: 16,
  });
  new google.maps.Marker({
    position: { lat: 53.3450082, lng: -6.272111 },
    map,
  });
}

// hide find job elements if no jobs found

let no_jobs = $(".no_jobs_title").css("display");
if (no_jobs === "block") {
  $(".page-count, .pagination").hide();
}

// validate employer job deleting form

$(".delete_job").on("click", function (e) {
  e.preventDefault();
  redirect_url = $(this).prop("href");
  //check for user confirmation
  $.confirm({
    title: "You are about to delete a job!",
    buttons: {
      confirm: function () {
        window.location.replace(redirect_url);
      },
      cancel: function () {},
    },
  });
});

// append cancel button to edit-job form

$(".edit-job-form").append($(".cancel-edit"));

// Send Email - Email.js

function sendMail(contactForm) {
  emailjs.send("service_z13soh8", "contact_form", {
    from_fName: contactForm.fName.value,
    from_lName: contactForm.lName.value,
    from_email: contactForm.emailaddress.value,
    message: contactForm.message.value,
    phone_number: contactForm.phoneNumber.value,
  });

  return false;
}

// refresh form after submit and show confirmation

$(".submit-form").click(function () {
  setTimeout(function () {
    $(".contact-form")[0].reset();
    $(".form-wrapper").append(
      `<div class="submit-message-box">
    <h3>Message submitted successfully</h3>
  </div>`
    );
    $(".submit-message-box").fadeOut(3000);
  }, 1000);
});

// reduce text lenght on mobile job listing
let click_count = 0;
$(".show-whole-description").click(function () {
  click_count++;
  $(this).parent().find("p").css("height", "100%");
  $(this).text("See Less");
  $(this).css("background", "#ffa62b");

  if (click_count % 2 == 0) {
    $(this).parent().find("p").css("height", "150px");
    $(this).text("See More");
    $(this).css("background", "#257e63");
  }
});
