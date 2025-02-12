import { checkAuth } from "/static/js/utils/checkAuth.js";

checkAuth("https://yumatsui.42.fr/home/", null);

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");
    const qrCodeUrl = params.get("qr_code_url");

    document.getElementById("verify-otp-btn").addEventListener("click", async () => {
        const otpCode = document.getElementById("otp").value.trim();

        if (!otpCode) {
            document.getElementById("otp-message").textContent = "Enter your OTP.";
            return;
        }

        try {
            const response = await fetch("https://yumatsui.42.fr/authenticator/verify_otp/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, otp: otpCode }) // ✅ `email` も送信
            });

            const data = await response.json();
            console.log(data)
            if (response.ok) {
                alert("２段階認証を承認しました");

                // ✅ OTP 認証成功後に再度 `login_view` を呼び出す
                const loginResponse = await fetch("https://yumatsui.42.fr/authenticator/login/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email: email })  // ✅ 2回目のログイン
                });

                const loginData = await loginResponse.json();

                if (loginResponse.ok) {
                    // ✅ JWT を保存
                    localStorage.setItem("access_token", loginData.access_token);
                    localStorage.setItem("refresh_token", loginData.refresh_token);

                    alert(`JWT トークン取得完了: ${loginData.access_token}`);
                    
                    // ✅ 認証後のページへリダイレクト
                    window.location.href = "https://yumatsui.42.fr/home/";
                } else {
                    alert("ログイン失敗！")
                }
            } else {
                document.getElementById("otp-message").textContent = data.message || "Invalid OTP.";
            }
        } catch (error) {
            console.error("OTP verification error:", error);
            document.getElementById("otp-message").textContent = "An error occurred. Please try again.";
        }
    });

    // ✅ 「Back to QR Code」ボタンを押したときに email & qr_code_url を URL に含める
    document.getElementById("back-to-qr-btn").addEventListener("click", () => {
        window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(email)}&qr_code_url=${encodeURIComponent(qrCodeUrl)}`;
    });
});

