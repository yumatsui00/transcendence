import { apiFetch, handleLogout } from "/static/js/utils/apiFetch.js";
import { checkAuth } from "/static/js/utils/checkAuth.js";
import { loadUserInfo, globalUserInfo } from "/static/js/utils/userInfo.js";
import { translations_format } from "/static/js/utils/translations.js";

// ✅ 認証チェック
checkAuth(null, "https://yumatsui.42.fr/");

// ✅ ローカルストレージから言語を取得 (デフォルト: 0)
const lang = parseInt(localStorage.getItem("language"), 10) || 0;
const translations = translations_format[lang] || translations_format[0];

// ✅ 設定ページの翻訳を適用
function applyTranslations() {
    document.title = translations.setting;
    document.getElementById("title").textContent = translations.usersettings;
    document.getElementById("backBtn").innerHTML = `<i class="bi bi-arrow-left"></i> ${translations.backtodefault}`;
    document.getElementById("changeProfileBtn").textContent = translations.changeprofile;
    document.getElementById("saveChangesBtn").textContent = translations.savechanges;
    document.getElementById("signOutBtn").textContent = translations.signout;
    document.querySelector("label[for='username']").textContent = translations.username;
    document.querySelector("label[for='email']").textContent = translations.email;
    document.querySelector("label[for='language']").textContent = translations.language;
}

applyTranslations();

// ✅ プロフィール情報のセットアップ
async function setupProfile() {
    localStorage.removeItem("user_info");
    await loadUserInfo(); // ✅ `userinfo` を取得

    if (globalUserInfo) {
        console.log("✅ ユーザー情報:", globalUserInfo);

        document.getElementById("username").value = globalUserInfo.username;
        document.getElementById("email").value = globalUserInfo.email;

        if (globalUserInfo.profile_image) {
            document.getElementById("profileImage").src = globalUserInfo.profile_image;  // ✅ URL をそのまま設定
        } else {
            document.getElementById("profileImage").src = "/static/images/default.png";  // ✅ デフォルト画像
        }

        console.log("image", globalUserInfo.profile_image)

        document.getElementById("language").value = globalUserInfo.language;
    }
}

// ✅ 画像アップロード処理
async function uploadProfileImage(file) {
    const formData = new FormData();
    formData.append("profile_image", file);

    try {
        const response = await apiFetch("https://yumatsui.42.fr/api/upload-profile/", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log("✅ プロフィール画像変更成功:", data);
            document.getElementById("profileImage").src = data.profile_image_url; // 新しい画像を表示
        } else {
            console.error("🚨 プロフィール画像アップロード失敗:", response.status);
        }
    } catch (error) {
        console.error("🚨 プロフィール画像アップロードエラー:", error);
    }
}

// ✅ 画像プレビュー機能
function previewProfileImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("profileImage").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

// ✅ ユーザー情報変更
async function changeUserInfo() {
    // パスワード入力用のモーダルを表示
    const password = prompt("🔑 Enter your password to confirm changes:");
    if (!password) {
        alert("⚠️ Password is required!");
        return;
    }

    // ✅ 入力データを取得
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const language = document.getElementById("language").value;
    const profileImage = document.getElementById("profileImage").src; // Base64 で送信

    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("language", language);
    formData.append("password", password);
    
    // 画像が変更されていれば送信
    if (profileImage.startsWith("data:image")) {
        formData.append("profile_image", profileImage);
    }

    try {
        const response = await apiFetch("https://yumatsui.42.fr/api/update-profile/", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            console.log("✅ ユーザー情報更新成功");
            alert("✅ User information updated successfully!");

            // ✅ 更新後のユーザー情報を再取得
            await setupProfile();
        } else {
            console.error("🚨 ユーザー情報更新失敗:", response.status, response.message);
            alert("❌ Failed to update user information.");
        }
    } catch (error) {
        console.error("🚨 ユーザー情報更新エラー:", error);
        alert("❌ Error updating user information.");
    }
}

// ✅ イベントリスナーを設定
document.addEventListener("DOMContentLoaded", async () => {
    await setupProfile();

    document.getElementById("backBtn").addEventListener("click", () => {
        window.location.href = "https://yumatsui.42.fr/home/";
    });

    document.getElementById("changeProfileBtn").addEventListener("click", () => {
        console.log("Change profile picture button clicked");
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = "image/*";
        fileInput.style.display = "none";
        document.body.appendChild(fileInput);

        fileInput.addEventListener("change", previewProfileImage);
        fileInput.click();
        fileInput.remove();
    });

    document.getElementById("saveChangesBtn").addEventListener("click", () => {
        changeUserInfo();
    });

    document.getElementById("signOutBtn").addEventListener("click", () => {
        handleLogout();
    });

    document.getElementById("language").addEventListener("change", (e) => {
        const selectedLang = parseInt(e.target.value, 10);
    });
});
