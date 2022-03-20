(function () {
    'use strict'
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
})()

function homepage() {
    var fraindesPage = document.getElementById("fraindes-page");
    var pageidentfier = document.getElementById("pageidentfier")
    var messagesPage = document.getElementById("messages-page");
    var fraindesCol = document.getElementById("fraindes-col");
    var messagesCol = document.getElementById("messages-col");
    var mediaQuery = window.matchMedia("(max-width: 768px)")
    console.log(">>>>>>>>>>>>>>>>>>>>>>>>")

    if (mediaQuery.matches) {
        if (pageidentfier.getAttribute("aria-expanded") == "false") {
            fraindesPage.style.display = "none";
            messagesPage.style.display = "flex";

            fraindesCol.style.display = "none";
            messagesCol.style.display = "flex";
            pageidentfier.setAttribute("aria-expanded", "true");

        } else {
            messagesCol.style.display = "none";
            fraindesPage.style.display = "flex";

            messagesPage.style.display = "none";
            fraindesCol.style.display = "flex";
            pageidentfier.setAttribute("aria-expanded", "false");

        }

    }

}

