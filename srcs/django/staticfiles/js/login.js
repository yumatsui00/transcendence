import { checkAuth } from "/static/js/utils/checkAuth.js";
import { translations_format } from "/static/js/utils/translations.js";
import { loginflow } from "/static/js/utils/loginflow.js";
import { getDeviceName } from "/static/js/utils/getDeviceName.js";


checkAuth("https://yumatsui.42.fr/home/", null);

const deviceName = getDeviceName();
const translations = translations_format
const lang = localStorage.getItem("selected_language") || 0;
document.getElementById('login-label').textContent = translations[lang].login;
document.getElementById('email-label').textContent = translations[lang].email
document.getElementById('pass-label').textContent = translations[lang].password;


document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // フォーム送信を防ぐ

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");
    console.log("Sending data:", { email, password, deviceName });

    loginflow(email, password, deviceName);
});

