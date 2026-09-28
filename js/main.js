document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Menu category jump-nav active state
  var jumpList = document.querySelector(".menu-jump-list");
  var jumpLinks = document.querySelectorAll(".menu-jump-list a");
  var categories = document.querySelectorAll(".menu-category");

  if (jumpList && categories.length && "IntersectionObserver" in window) {
    var map = {};
    jumpLinks.forEach(function (a) {
      map[a.getAttribute("href").replace("#", "")] = a;
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var link = map[entry.target.id];
          if (!link) return;
          if (entry.isIntersecting) {
            jumpLinks.forEach(function (a) {
              a.classList.remove("is-active");
            });
            link.classList.add("is-active");
            // Scroll only the pill bar; scrollIntoView would also drag the page back to the bar.
            jumpList.scrollTo({
              left: link.offsetLeft - (jumpList.clientWidth - link.offsetWidth) / 2,
              behavior: "smooth"
            });
          }
        });
      },
      { rootMargin: "-160px 0px -70% 0px", threshold: 0 }
    );

    categories.forEach(function (cat) {
      observer.observe(cat);
    });
  }
});
