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

document.addEventListener("DOMContentLoaded", function () {
  // Handle sidebar toggle
  const sidebar = document.getElementById("nav-sidebar");
  const closeBtn = document.querySelector(".closeSidebar");

  // Toggle sidebar when clicking on close button
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });
  }

  // Make bottom nav buttons open sidebar
  const menuIcons = document.querySelectorAll(".nav-sidebar1 i.fas");
  menuIcons.forEach((icon) => {
    icon.addEventListener("click", function (e) {
      if (window.innerWidth <= 568) {
        e.preventDefault();
        sidebar.classList.add("active");
      }
    });
  });
});
function showEditTask(taskId) {
  // First hide more options menu
  HideMoreOptions();

  // Show the existing add task form
  const addTask = document.querySelector(".addTask");
  if (addTask) {
    addTask.style.display = "block";

    // Get the form element
    const form = addTask.querySelector("form");
    if (form) {
      // Change form action to update
      form.action = `/update/${taskId}`;

      // Find the task element by ID to get its data
      const moreOptions = document.getElementById("moreOptions_" + taskId);
      if (moreOptions) {
        // Get the task container
        const taskContainer = moreOptions.nextElementSibling;
        if (taskContainer) {
          // Extract title
          const titleElement = taskContainer.querySelector("h4");
          if (titleElement) {
            form.querySelector('input[name="title"]').value =
              titleElement.textContent.trim();
          }

          // Extract description
          const descElement = taskContainer.querySelector("p");
          if (descElement) {
            form.querySelector('input[name="description"]').value =
              descElement.textContent.trim();
          }

          // Extract date if available
          const dateElement = taskContainer.querySelector("span");
          if (dateElement) {
            const dateText = dateElement.textContent.trim();
            // Remove the calendar icon text if present
            const cleanDateText = dateText.replace("Today", "").trim();

            // Set the value in the date input
            const dateInput = form.querySelector('input[id="datetimepicker"]');
            if (dateInput) {
              dateInput.value = cleanDateText;
              // Change the name attribute to match what the server expects
              dateInput.name = "dueDate";
            }
          }
        }
      }

      // Change button text
      const button = form.querySelector("#add-btn span");
      if (button) {
        button.textContent = "Update Task";
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Get all navigation items in the mobile nav
  const mobileNavItems = document.querySelectorAll(".nav-sidebar1 li");

  // Add click handlers to each item
  mobileNavItems.forEach(function (item) {
    // Skip the item that already has an onclick attribute (search)
    if (item.hasAttribute("onclick")) {
      return; // Skip this item to preserve its original onclick behavior
    }

    item.addEventListener("click", function (e) {
      // Get the link inside this nav item
      const link = item.querySelector("a");

      // Navigate to the link's href
      if (link) {
        window.location.href = link.getAttribute("href");
      }
    });
  });
});
