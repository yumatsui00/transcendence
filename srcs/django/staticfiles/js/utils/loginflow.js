export async function loginflow(email, password, deviceName) {
    const loginResponse = await fetch("https://yumatsui.42.fr/authenticator/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, password: password, device: deviceName })
    })
    if (loginResponse.ok) {
        const loginData = await loginResponse.json();
        if (loginData.requires_2fa) {
            // 2FA認証が必要
            if (loginData.is_registered_once) {
                // 2FA認証を行ったことがある→OTP入力へ
                window.location.href = `https://yumatsui.42.fr/authenticator/otp/?email=${encodeURIComponent(email)}}`;
            } else {
                // 2FA認証を行ったことがない→qr登録へ
                window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(email)}}`;
            }
        } else {
            //2FA認証が不必要→homeへ
            localStorage.setItem("access_token", loginData.access_token);
            localStorage.getItem("refresh_token", loginData.refresh_token);
            window.location.href = "https://yumatsui.42.fr/home/"
        }
    } else {
        alert("ログイン失敗！")
    }
}
