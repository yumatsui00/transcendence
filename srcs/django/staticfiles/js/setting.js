import { apiFetch, handleLogout } from "/static/js/utils/apiFetch.js" 
import { checkAuth } from "/static/js/utils/checkAuth.js";

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("logout-button").addEventListener("click", function () {
        handleLogout()
    });
});
