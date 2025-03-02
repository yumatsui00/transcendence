document.addEventListener("DOMContentLoaded", function () {
    const profileImage = document.getElementById("profileImage");
    const changeProfileBtn = document.getElementById("changeProfileBtn");
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const languageSelect = document.getElementById("language");
    const saveChangesBtn = document.getElementById("saveChangesBtn");
    const signOutBtn = document.getElementById("signOutBtn");

    // ✅ ローディング画面を表示
    document.getElementById("loading-screen").style.display = "none";

    // ✅ ローカルストレージからユーザー情報を取得（仮）
    usernameInput.value = localStorage.getItem("username") || "";
    emailInput.value = localStorage.getItem("email") || "";
    languageSelect.value = localStorage.getItem("language") || "0";

    // ✅ 画像変更ボタン（ファイル選択）
    changeProfileBtn.addEventListener("click", function () {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = "image/*";
        fileInput.addEventListener("change", function () {
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profileImage.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
        fileInput.click();
    });

    // ✅ 設定を保存
    saveChangesBtn.addEventListener("click", function () {
        localStorage.setItem("username", usernameInput.value);
        localStorage.setItem("email", emailInput.value);
        localStorage.setItem("language", languageSelect.value);
        alert("Settings saved successfully!");
    });

    // ✅ ログアウト処理
    signOutBtn.addEventListener("click", async function () {
        try {
            const logoutResponse = await fetch("https://localhost:8443/api/logout/", {
                method: "POST",  // ✅ ログアウトは `POST` のほうが適切
                credentials: "include"  // ✅ クッキーを含める（重要）
            });

            if (logoutResponse.ok) {
                alert("Logged out successfully!");
                window.location.href = "https://localhost:8443";  // ✅ ルートページへリダイレクト
            } else {
                alert("Logout failed! Please try again.");
            }
        } catch (error) {
            console.error("Logout error:", error);
            alert("An error occurred. Please try again.");
        }
    });
});
