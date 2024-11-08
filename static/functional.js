const navSidebar = document.getElementById("nav-sidebar");
const toggleButton = document.getElementById("toggleButton");

function ShowMoreOptions(taskId) {
  const ellipsisOnclick = document.querySelectorAll(".moreOptions");

  Array.from(ellipsisOnclick).forEach(
    (ellipse) => (ellipse.style.display = "none")
  );

  const selectedoptions = document.querySelector(`#moreOptions_${taskId}`);
  if (selectedoptions) {
    selectedoptions.style.display = "block";
  }
}
function HideMoreOptions() {
  const ellipsisOnclick = document.querySelectorAll(".moreOptions");

  Array.from(ellipsisOnclick).forEach(
    (ellipse) => (ellipse.style.display = "none")
  );
}

function showAddbar() {
  const Addbar = document.querySelector(".addTask");
  Addbar.style.display = "block";
}
function hideAddbar() {
  console.log("hiding addbar");
  const Addbar = document.querySelector(".addTask");
  Addbar.style.display = "none";
}

var ellipsisMouseOver = document.getElementById("addTask-pstn");
var ellipsisElements = document.querySelectorAll(".ellipsis");

ellipsisElements.forEach(function (ellipsis) {
  parentLi = ellipsis.closest("li");
  parentLi.addEventListener("mouseover", function () {
    ellipsis.style.display = "inline";
  });
  parentLi.addEventListener("mouseout", function () {
    ellipsis.style.display = "none";
  });
});

function showEditTask(taskId) {
  var editForm = document.getElementById("editTask_" + taskId);

  if (editForm) {
    editForm.style.display = "block";
  }
}
function hideEditTask() {
  const editTask = document.querySelector(".editTask");
  if (editTask) {
    editTask.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const defaultDate = new Date("{{currentDate}}");
  flatpickr("#currentDatePickr", {
    dateFormat: "M j",
    defaultDate: defaultDate,
  });
});

function showSearchbar() {
  const searchBar = document.querySelector(".searchbar");
  searchBar.style.display = "block";
}
function hideSearchbar() {
  const searchBar = document.querySelector(".searchbar");
  searchBar.style.display = "none";
}
document
  .querySelector(".searchbar")
  .addEventListener("click", function (event) {
    event.stopPropagation();
    const searchBar = document.querySelector(".searchbar");
    if (searchBar.display.style === "block") {
      hideSearchbar();
    } else {
      showSearchbar();
    }
  });

document.addEventListener("click", (event) => {
  const searchBar = document.querySelector(".searchbar");
  if (
    !searchBar.contains(event.target) &&
    !event.target.matches(".search-icon")
  ) {
    hideSearchbar();
  }
});
function showSearchbar1() {
  document.getElementById("fixedElement").searchBar.style.display = "block";
}
function showSearchbar_beforeSubmit(event) {
  event.preventDefault;
  document.getElementById("fixedElement").searchBar.style.display = "block";
}

function hideMessage(element) {
  const flashedMessage = element.closest("li");
  if (flashedMessage) {
    flashedMessage.style.display = "none";
  }
}
function setSearchTerm(term) {
  document.getElementById("searchinput").value = term;
}
