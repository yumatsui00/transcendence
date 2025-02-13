import { checkAuth } from "/static/js/utils/checkAuth.js";
import { translations_format } from "/static/js/utils/translations.js" 

checkAuth("https://yumatsui.42.fr/home/", null);

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
    console.log("Sending data:", { email, password });

    try {
        const response = await fetch("https://yumatsui.42.fr/authenticator/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email, password: password })
        });

        const data = await response.json();
        console.log("Response data:", data);

        if (response.ok) {
            alert("ログイン成功！"); // ✅ 成功時のみ表示
            console.log("シュトクdata: ", data);

            // ✅ 2FA が必要なら QR コードページへ
            if (data.requires_2fa) {
                window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(data.email)}&qr_code_url=${encodeURIComponent(data.qr_code_url)}`;
            } else {
                // ✅ JWT トークン保存
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                console.log("JWT トークン取得完了:", data.access_token);
                
                // ✅ 認証後のページへリダイレクト
                window.location.href = "https://yumatsui.42.fr/home/";
            }
        } else {
            // ❌ 失敗時の処理
            errorMessage.textContent = data.message || "ログインに失敗しました。";
            errorMessage.style.display = "block";
        }
    } catch (error) {
        // ❌ サーバーエラー時の処理
        errorMessage.textContent = "サーバーに接続できませんでした。";
        errorMessage.style.display = "block";
        console.error("エラー:", error);
    }
});
