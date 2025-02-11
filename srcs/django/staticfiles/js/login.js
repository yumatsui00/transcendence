document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // フォーム送信を防ぐ

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    // // 簡単なバリデーション
    // if (!email.includes("@")) {
    //     errorMessage.textContent = "正しいメールアドレスを入力してください。";
    //     errorMessage.style.display = "block";
    //     return;
    // }

    if (password.length < 8) {
        errorMessage.textContent = "パスワードは8文字以上入力してください。";
        errorMessage.style.display = "block";
        return;
    }

    // バリデーション成功
    errorMessage.style.display = "none";


    try {
        const response = await fetch("https://yumatsui.42.fr/authenticator/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("ログイン成功！"); // 成功時の処理（リダイレクトなど）
            console.log("シュトクdata: ", data)
            //TODO responseの2fa_requiresがTrueなら2fa
            if (data.requires_2fa) {
                window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(data.email)}&qr_code_url=${encodeURIComponent(data.qr_code_url)}`
            } else {
                //TODO jwt Token
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                console.log("JWT トークン取得完了:", data.access_token);
                // ✅ 認証後のページへリダイレクト
                window.location.href = "https://yumatsui.42.fr/home/";
            }
        } else {
            errorMessage.textContent = data.message || "ログインに失敗しました。";
            errorMessage.style.display = "block";
        }
    } catch (error) {
        errorMessage.textContent = "サーバーに接続できませんでした。";
        errorMessage.style.display = "block";
        console.error("エラー:", error);
    }


    alert("ログイン成功！（仮）");
});
