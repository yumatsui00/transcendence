import { getUserInfo } from "./getUserInfo.js"

let globalUserInfo = JSON.parse(localStorage.getItem("user_info")) || null;

async function loadUserInfo() {
    if (globalUserInfo) {
        console.log("✅ キャッシュからユーザー情報を取得:", globalUserInfo);
        return globalUserInfo;
    }


    try {
        globalUserInfo = await getUserInfo();
        if (!globalUserInfo) {
            console.warn("🚨 ユーザー情報が取得できませんでした");
            window.location.href = "/";
            return null;
        }

        // ✅ `localStorage` に保存
        localStorage.setItem("user_info", JSON.stringify(globalUserInfo));

        console.log("✅ API からユーザー情報を取得:", globalUserInfo);
        return globalUserInfo;
    } catch (error) {
        console.error("🚨 ユーザー情報の取得中にエラー:", error);
        window.location.href = "/login/";
    } finally {
        document.getElementById("loading-screen").style.display = "none";
    }
}

export { loadUserInfo, globalUserInfo };