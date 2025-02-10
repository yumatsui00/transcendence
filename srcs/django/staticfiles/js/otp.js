document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");
    const qrCodeUrl = params.get("qr_code_url");

    console.log("Email:", email);
    console.log("QR Code URL:", qrCodeUrl);

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
            if (response.ok) {
                alert("OTP Verified! Redirecting to dashboard.");
                //TODO login flow
                window.location.href = "/home"; // 認証成功後のリダイレクト
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

