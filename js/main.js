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
  var jumpLinks = document.querySelectorAll(".menu-jump-list a");
  var categories = document.querySelectorAll(".menu-category");

  if (jumpLinks.length && categories.length && "IntersectionObserver" in window) {
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
            link.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
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
