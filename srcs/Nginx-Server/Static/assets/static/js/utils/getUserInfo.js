import { apiFetch } from "./apiFetch.js";

export async function getUserInfo() {
    try {
        const response = await apiFetch("https://localhost:8443/api/userinfo/");
        if (response.ok) {
            const userInfo = await response.json();
            console.log("✅ ユーザー情報取得成功:", userInfo);

            // ✅ ユーザー情報を localStorage に保存（オプション）
            localStorage.setItem("user_info", JSON.stringify(userInfo));

            return userInfo;
        } else {
            console.error("🚨 ユーザー情報の取得に失敗:", response.status);
            return null;
        }
    } catch (error) {
        console.error("🚨 ユーザー情報の取得中にエラー:", error);
        return null;
    }
}

