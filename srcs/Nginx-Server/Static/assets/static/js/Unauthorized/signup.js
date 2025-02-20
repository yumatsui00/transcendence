// import { loginflow } from "./utils/loginflow.js";
// import { checkAuth } from "/static/js/utils/checkAuth.js";
import { translations_format } from "/static/js/utils/translations.js";
import { getDeviceName } from "/static/js/utils/getDeviceName.js";


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
    const color = 0;
    const language = lang
    const is_2fa_enabled = document.getElementById("enable-2fa").checked;
    const deviceName = getDeviceName();

    // ✅ `FormData` を使用してデータを送信
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", userEmail);
    formData.append("password", password);
    formData.append("language", language);
    formData.append("color", color);
    formData.append("is_2fa_enabled", is_2fa_enabled);

    try {
        console.log("Sending data:", Object.fromEntries(formData.entries())); // 🔍 送信データを確認
        const response = await fetch("https://yumatsui.42.fr/user/signup/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        messageBox.textContent = data.message;
        console.log("Response Data:", data); 

        // if (response.ok) {
        //     loginflow(userEmail, password, deviceName);
        // } else {
        //     console.log(data)
        //     alert("signup失敗")
        // }
    } catch (error) {
        console.error("Error:", error);
        messageBox.textContent = "Signup failed";
    }
});

