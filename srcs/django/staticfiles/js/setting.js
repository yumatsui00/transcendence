import { apiFetch, handleLogout } from "/static/js/utils/apiFetch.js" 
import { checkAuth } from "/static/js/utils/checkAuth.js";
import { loadUserInfo, globalUserInfo } from "/static/js/utils/userInfo.js";

// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById("logout-button").addEventListener("click", function () {
//         handleLogout()
//     });
// });


checkAuth(null, "https://yumatsui.42.fr/")

async function setupProfile() {
    localStorage.removeItem("user_info");
    await loadUserInfo(); // ✅ `userinfo` を取得

    if (globalUserInfo) {
        console.log("✅ ユーザー情報:", globalUserInfo);

        // ✅ HTML の `input` にユーザー情報を埋め込む
        document.getElementById("username").value = globalUserInfo.username;
        document.getElementById("email").value = globalUserInfo.email;

        // ✅ プロフィール画像があれば表示
        if (globalUserInfo.profile_image) {
            document.getElementById("profileImage").src = globalUserInfo.profile_image;
        }

        // ✅ 2FA のチェックボックス
        document.getElementById("twoFA").checked = globalUserInfo.is_2fa_enabled;

        // ✅ 言語の選択
        document.getElementById("language").value = globalUserInfo.language;
    }
}

// document.addEventListener("DOMContentLoaded", setupProfile);



document.addEventListener("DOMContentLoaded", async () => {
    await setupProfile();

    const backBtn = document.getElementById("backBtn");
    const changeProfileBtn = document.getElementById("changeProfileBtn");
    const saveChangesBtn = document.getElementById("saveChangesBtn");
    const signOutBtn = document.getElementById("signOutBtn");
    const twoFAToggle = document.getElementById("twoFA");
    const languageSelect = document.getElementById("language");

    backBtn.addEventListener("click", () => {
        window.location.href = "https://yumatsui.42.fr/home/";
    });

    changeProfileBtn.addEventListener("click", () => {
        console.log("Change profile picture button clicked");
    });

    saveChangesBtn.addEventListener("click", () => {
        console.log("Save changes button clicked");
    });

    signOutBtn.addEventListener("click", () => {
        handleLogout();
        console.log("Sign out button clicked");
    });

    twoFAToggle.addEventListener("change", (e) => {
        console.log("Two-Factor Authentication:", e.target.checked ? "Enabled" : "Disabled");
    });

    languageSelect.addEventListener("change", (e) => {
        console.log("Language changed to:", e.target.value);
    });
});
