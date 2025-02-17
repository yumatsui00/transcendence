import { apiFetch } from "./apiFetch.js";

/**
 * ユーザーの認証状態をチェックし、必要ならリダイレクト
 * @param {string|null} authRedirect - 認証済みユーザーのリダイレクト先（nullならリダイレクトなし）
 * @param {string|null} noAuthRedirect - 未認証ユーザーのリダイレクト先（nullならリダイレクトなし）
 */
export async function checkAuth(authRedirect = null, noAuthRedirect = null) {
    const access_token = localStorage.getItem("access_token");
    console.log("🔍 Checking Auth...");
    console.log("🔍 Access Token:", access_token);
    document.body.classList.add("loading");

    if (!access_token) {
        console.warn("🚨 No access token found.");
        if (noAuthRedirect) {
            window.location.href = noAuthRedirect;
            return ;
        }
        document.getElementById("loading-screen").style.display = "none";  // 🔹 ここで非表示にする
        document.body.classList.remove("loading");
        return;
    }
    

    try {
        const response = await apiFetch("../authenticator/check_auth/");

        if (response.ok) {
            const data = await response.json();
            if (data.is_authenticated) {
                console.log("✅ ユーザーはログイン済み");
                if (authRedirect) {
                    window.location.href = authRedirect;
                    return ;
                }
            } else {
                console.log("🚨 ユーザーは未認証");
                alert("1")
                if (noAuthRedirect) {
                    window.location.href = noAuthRedirect;
                    return ;
                }
            }
        } else {
            console.error("🚨 認証チェックに失敗 (JWT 失効の可能性あり)", response.status);
            console.log(response.status);

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            alert("2")
            if (noAuthRedirect) {
                window.location.href = noAuthRedirect;
                return ;
            }
        }
    } catch (error) {
        console.error("🚨 認証リクエスト中にエラー:", error);
    }
    document.getElementById("loading-screen").style.display = "none";
    document.body.classList.remove("loading");
}
