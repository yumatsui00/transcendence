// import { loginflow } from "./utils/loginflow.js";
// import { checkAuth } from "/static/js/utils/checkAuth.js";
import { translations_format } from "/static/js/utils/translations.js";
import { getDeviceName } from "/static/js/utils/getDeviceName.js";

async function signupflow(username, email, password, is_2fa_enabled, language, deviceName) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("language", language);
    formData.append("password", password);
    formData.append("is_2fa_enabled", is_2fa_enabled);

    try {
        if (!username || username.length > 10) {
            alert("ユーザーネームは１〜１０文字以内で入力してください")
            return ;
        }
        //! email check

        console.log("Sending data:", Object.fromEntries(formData.entries())); // 🔍 送信データを確認
        const response = await fetch("https://yumatsui.42.fr/api/signup/", {
            method: "POST",
            body: formData
        });

        const data = await response.json()
        messageBox.textContent = data.message;
        if (response.ok) {
            //login flow
        }
    } catch (error) {
        console.error("Error: ", error);
        message.textContent = "SignUp Failed";
    }
}

// checkAuth("https://yumatsui.42.fr/home/", null);

const translations = translations_format
const lang = localStorage.getItem("selected_language") || 0;
document.getElementById('signup-label').textContent = translations[lang].signup;
document.getElementById('username-label').textContent = translations[lang].username;
document.getElementById('email-label').textContent = translations[lang].email;
document.getElementById('password-label').textContent = translations[lang].password;
document.getElementById('2fa-label').textContent = translations[lang].twofa;
document.getElementById('signupBtn-label').textContent = translations[lang].signup;

const messageBox = document.getElementById("message");

document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // フォーム送信を防ぐ


    const username = document.getElementById("username").value;
    const userEmail = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const language = lang
    const is_2fa_enabled = document.getElementById("enable-2fa").checked;
    const deviceName = getDeviceName();

    signupflow(username, userEmail, password, is_2fa_enabled, language, deviceName)

});

