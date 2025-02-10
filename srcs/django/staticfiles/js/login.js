document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        console.error("Error: #loginForm が見つかりません。HTMLにフォームがあるか確認してください。");
        return;
    }

    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // フォーム送信を防ぐ
        console.log("フォーム送信イベントが発生しました！");

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const errorMessage = document.getElementById("error-message");

        if (password.length < 8) {
            errorMessage.textContent = "パスワードは8文字以上入力してください。";
            errorMessage.style.display = "block";
            return;
        }

        errorMessage.style.display = "none";

        try {
            const response = await fetch("https://yumatsui.42.fr/authenticator/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("ログイン成功！"); // 成功時の処理（リダイレクトなど）

                if (data.requires_2fa) {
                    window.location.href = `https://yumatsui.42.fr/authenticator/qr/?email=${encodeURIComponent(data.email)}&qr_code_url=${encodeURIComponent(data.qr_code_url)}`;
                } else {
                    // TODO: JWT Token の処理
                }
                console.log("レスポンス:", data);
            } else {
                errorMessage.textContent = data.message || "ログインに失敗しました。";
                errorMessage.style.display = "block";
            }
        } catch (error) {
            errorMessage.textContent = "サーバーに接続できませんでした。";
            errorMessage.style.display = "block";
            console.error("エラー:", error);
        }
    });

    console.log("ログインフォームのイベントリスナーが設定されました！");
});
