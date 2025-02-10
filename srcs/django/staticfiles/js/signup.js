document.addEventListener("DOMContentLoaded", () => {
    // ✅ モーダル要素を取得
    const qrModalElement = document.getElementById("qr-modal");
    const otpModalElement = document.getElementById("otp-modal");
    const qrCodeImg = document.getElementById("qr-code");
    const closeQrButton = document.getElementById("close-qr");
    const otpInput = document.getElementById("otp");
    const verifyOtpButton = document.getElementById("verify-otp-button");
    const messageBox = document.getElementById("otp-message");
    const signupButton = document.getElementById("signupBtn");

    let userEmail = "";


    // ✅ プロフィール画像のプレビュー機能
    document.getElementById("profile_image").addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("imagePreview").src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    // ✅ デフォルト画像に戻す
    document.getElementById("initimgBtn").addEventListener("click", function () {
        document.getElementById("imagePreview").src = "/static/images/default.png";
        document.getElementById("profile_image").value = "";
    });


    // ✅ サインアップ処理
    signupButton.addEventListener("click", async function () {
        const username = document.getElementById("username").value;
        userEmail = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const language = document.getElementById("language").value;
        const color = 0;
        const profileImage = document.getElementById("profile_image").files[0];
        const is_2fa_enabled = document.getElementById("enable-2fa").checked;

        if (!username || !userEmail || !password) {
            messageBox.textContent = "All fields are required";
            return;
        }

        const formData = new FormData();
        formData.append("username", username);
        formData.append("email", userEmail);
        formData.append("password", password);
        formData.append("language", language);
        formData.append("color", color);
        if (profileImage) {
            formData.append("profile_image", profileImage);
        }
        formData.append("is_2fa_enabled", is_2fa_enabled);

        try {
            const response = await fetch("https://yumatsui.42.fr/authenticator/signup/", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            messageBox.textContent = data.message;

            if (response.ok) {
                if (data.is_2fa_enabled) {
                    alert("SignUp has done successfully! Generating QR code for 2FA");
                    
                    // ✅ QRコードをセットして表示
                    qrCodeImg.src = data.qr_code_url;
                    const qrModal = new bootstrap.Modal(qrModalElement);
                    qrModal.show();

                    // ✅ QRコードを閉じたら OTP モーダルを表示
                    qrModalElement.addEventListener("hidden.bs.modal", () => {
                        console.log("QRモーダル閉じられた → OTPモーダルを開く");
                        const otpModal = new bootstrap.Modal(otpModalElement);
                        otpModal.show();
                    });

                } else {
                    alert("SignUp has done successfully! Redirecting to login");
                    window.location.href = "/login"; // 2FAなしならログイン画面へ
                }
            }
        } catch (error) {
            console.error("Error:", error);
            messageBox.textContent = "Signup failed";
        }
    });

    // ✅ QRコードモーダルを閉じたら OTP 入力モーダルを表示
    closeQrButton.addEventListener("click", () => {
        console.log("QRモーダル閉じるボタンがクリックされた");

        // QRモーダルを取得し閉じる
        const qrModal = bootstrap.Modal.getInstance(qrModalElement);
        if (qrModal) {
            qrModal.hide();
        } else {
            console.error("QRモーダルが取得できませんでした");
        }

        // OTPモーダルを開く
        const otpModal = new bootstrap.Modal(otpModalElement);
        otpModal.show();

        // 入力欄をクリア
        otpInput.value = "";
        messageBox.textContent = "";
    });

    // ✅ OTP 認証処理
    verifyOtpButton.addEventListener("click", async function () {
        const otpCode = otpInput.value.trim(); // 空白除去

        if (!otpCode) {
            messageBox.textContent = "ワンタイムパスワードを入力してください。";
            messageBox.style.color = "red";
            return;
        }

        try {
            const response = await fetch("/authenticator/verify_otp/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: userEmail, otp: otpCode })
            });

            const data = await response.json();

            if (response.ok) {
                alert("OTP 認証成功！ダッシュボードへ移動します。");
                window.location.href = "/dashboard"; // 認証成功後のリダイレクト
            } else {
                messageBox.textContent = data.message || "OTP 認証に失敗しました。";
                messageBox.style.color = "red";
            }
        } catch (error) {
            console.error("OTP verification error:", error);
            messageBox.textContent = "エラーが発生しました。もう一度試してください。";
            messageBox.style.color = "red";
        }
    });
});

