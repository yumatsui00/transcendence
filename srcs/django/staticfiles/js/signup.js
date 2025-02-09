document.getElementById("signupBtn").addEventListener("click", async function () {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const language = document.getElementById("language").value;
    const color = 0;
    const profileImage = document.getElementById("profile_image").files[0];  // ✅ 画像を取得

    if (!username || !email || !password) {
        document.getElementById("message").textContent = "All fields are required";
        return;
    }

    // ✅ `FormData` を使用してデータを送信
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("language", language);
    formData.append("color", color);

    if (profileImage) {
        formData.append("profile_image", profileImage);  // ✅ 画像がある場合は追加
    }

    try {
        // ✅ `Content-Type` を `multipart/form-data` にするため、`headers` は設定しない
        const response = await fetch("https://yumatsui.42.fr/signup/", {
            method: "POST",
            body: formData  // ✅ `FormData` をそのまま送信
        });

        const data = await response.json();
        document.getElementById("message").textContent = data.message;

        if (data.success) {
            // ✅ 保存されたプロフィール画像のURLを取得し、表示する
            localStorage.setItem("profile_image_url", data.profile_image_url);
            window.location.href = "/home/";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("message").textContent = "Signup failed";
    }
});


document.getElementById("profile_image").addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("imagePreview").src = e.target.result; // ✅ プレビュー画像を表示
        };
        reader.readAsDataURL(file);
    }
});
