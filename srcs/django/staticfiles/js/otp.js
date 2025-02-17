<<<<<<< HEAD
=======
import { getDeviceName } from "/static/js/utils/getDeviceName.js";

>>>>>>> main
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");
    const isRegisteredOnce = params.get("is_registered_once") === "true"; // ✅ 文字列なので変換
    const deviceName = getDeviceName()

    // ✅ `is_registered_once` が `true` の場合、戻るボタンを削除
    if (isRegisteredOnce) {
        document.getElementById("back-to-qr-btn").style.display = "none";
    }

    document.getElementById("verify-otp-btn").addEventListener("click", async () => {
        const otpCode = document.getElementById("otp").value.trim();

        if (!otpCode) {
            document.getElementById("otp-message").textContent = "Enter your OTP.";
            return;
        }

        try {
            const response = await fetch("../authenticator/verify_otp/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, otp: otpCode, device: deviceName }) // ✅ `email` も送信
            });

            const data = await response.json();
            console.log(data)
            if (response.ok) {
                alert("２段階認証を承認しました");
<<<<<<< HEAD

                // ✅ OTP 認証成功後に再度 `login_view` を呼び出す
                const loginResponse = await fetch("../authenticator/login/", {
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
                    window.location.href = "../..//home/";
                } else {
                    alert("ログイン失敗！")
                }
=======
                localStorage.setItem("access_token", data.access_token);
                localStorage.getItem("refresh_token", data.refresh_token);
                localStorage.setItem("language", data.lang);
                window.location.href = "https://yumatsui.42.fr/home/";
>>>>>>> main
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
<<<<<<< HEAD
        window.location.href = `../authenticator/qr/?email=${encodeURIComponent(email)}&qr_code_url=${encodeURIComponent(qrCodeUrl)}`;
=======
        window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(email)}}`;
>>>>>>> main
    });
});

