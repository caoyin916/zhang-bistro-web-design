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

  // Dish photo dialog on the menu page
  var dialog = document.getElementById("dishDialog");
  var menuRoot = document.querySelector(".menu-categories");

  if (dialog && menuRoot && typeof dialog.showModal === "function") {
    var media = dialog.querySelector(".dish-dialog-media");
    var catEl = dialog.querySelector(".dish-dialog-cat");
    var titleEl = dialog.querySelector("#dishDialogTitle");
    var priceEl = dialog.querySelector(".dish-dialog-price");
    var cnEl = dialog.querySelector(".dish-dialog-cn");
    var flagsEl = dialog.querySelector(".dish-dialog-flags");

    var el = function (tag, className, text) {
      var node = document.createElement(tag);
      if (className) node.className = className;
      if (text) node.textContent = text;
      return node;
    };

    var openDish = function (item) {
      var en = item.querySelector(".menu-item-en").firstChild.textContent.trim();
      var cn = item.querySelector(".menu-item-cn").textContent;
      var photo = item.getAttribute("data-photo");

      media.replaceChildren();
      if (photo) {
        var img = el("img");
        img.src = photo;
        img.alt = en + " (" + cn + ")";
        media.appendChild(img);
      } else {
        var placeholder = el("div", "dish-dialog-placeholder");
        var logo = el("img");
        logo.src = "assets/img/logo-mark.png";
        logo.alt = "";
        placeholder.append(logo, el("strong", "", "Picture coming soon"), el("span", "cn", "图片即将上线"));
        media.appendChild(placeholder);
      }

      catEl.textContent = item.closest(".menu-category").querySelector(".menu-category-head span").textContent;
      titleEl.textContent = en;
      priceEl.textContent = item.querySelector(".menu-item-price").textContent;
      cnEl.textContent = cn;
      flagsEl.replaceChildren.apply(
        flagsEl,
        Array.prototype.map.call(item.querySelectorAll(".pop-flag, .soldout-flag"), function (f) {
          return f.cloneNode(true);
        })
      );

      document.documentElement.classList.add("dialog-open");
      dialog.showModal();
    };

    menuRoot.addEventListener("click", function (e) {
      var item = e.target.closest(".menu-item");
      if (item) openDish(item);
    });

    dialog.addEventListener("click", function (e) {
      if (e.target === dialog || e.target.closest("[data-dialog-close]")) dialog.close();
    });

    dialog.addEventListener("close", function () {
      document.documentElement.classList.remove("dialog-open");
    });
  }

  // Live open/closed badge, computed in Carrollton time. Mon closed; Tue–Sun 11 AM–10 PM.
  var statusEls = document.querySelectorAll("[data-open-status]");

  if (statusEls.length && window.Intl) {
    var OPEN_MIN = 11 * 60;
    var CLOSE_MIN = 22 * 60;
    var CLOSED_DAYS = [1];
    var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var fmt = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Chicago",
      weekday: "short",
      hour: "numeric",
      minute: "numeric",
      hourCycle: "h23"
    });

    var carrolltonNow = function () {
      var parts = {};
      fmt.formatToParts(new Date()).forEach(function (p) {
        parts[p.type] = p.value;
      });
      return { day: DAYS.indexOf(parts.weekday), minutes: (+parts.hour % 24) * 60 + +parts.minute };
    };

    var openStatus = function (now) {
      var openToday = CLOSED_DAYS.indexOf(now.day) === -1;
      if (openToday && now.minutes >= OPEN_MIN && now.minutes < CLOSE_MIN) {
        return CLOSE_MIN - now.minutes <= 30
          ? { state: "closing", text: "Closing soon · 10 PM" }
          : { state: "open", text: "Open now · closes 10 PM" };
      }
      if (openToday && now.minutes < OPEN_MIN) {
        return { state: "closed", text: "Closed · opens 11 AM" };
      }
      for (var d = 1; d <= 7; d++) {
        var day = (now.day + d) % 7;
        if (CLOSED_DAYS.indexOf(day) === -1) {
          return { state: "closed", text: "Closed · opens " + (d === 1 ? "tomorrow" : DAYS[day]) + " 11 AM" };
        }
      }
    };

    var renderStatus = function () {
      var s = openStatus(carrolltonNow());
      statusEls.forEach(function (node) {
        node.setAttribute("data-state", s.state);
        node.querySelector(".open-status-text").textContent = s.text;
      });
    };

    renderStatus();
    setInterval(renderStatus, 60000);
  }
});
