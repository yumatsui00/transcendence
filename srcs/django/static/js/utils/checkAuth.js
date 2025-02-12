import { apiFetch } from "./apiFetch.js";

/**
 * ユーザーの認証状態をチェックし、必要ならリダイレクト
 * @param {string|null} authRedirect - 認証済みユーザーのリダイレクト先（nullならリダイレクトなし）
 * @param {string|null} noAuthRedirect - 未認証ユーザーのリダイレクト先（nullならリダイレクトなし）
 */
export async function checkAuth(authRedirect = null, noAuthRedirect = null) {
    const access_token = localStorage.getItem("access_token");
	console.log("arrived checkAuth");
    console.log(`accesstoken: ${access_token}`);
    document.body.classList.add("loading");

    if (!access_token) {
        console.warn("🚨 No access token found.");
        document.getElementById("loading-screen").style.display = "none";  // 🔹 ここで非表示にする
        document.body.classList.remove("loading");
        if (noAuthRedirect) {
            window.location.href = noAuthRedirect;
        }
        return;
    }
    

    try {
        const response = await apiFetch("https://yumatsui.42.fr/authenticator/check_auth/");

        if (response.ok) {
            const data = await response.json();
            if (data.is_authenticated) {
                console.log("✅ ユーザーはログイン済み");
                if (authRedirect) {
                    document.body.classList.remove("loading");
                    window.location.href = authRedirect;
                    return ;
                }
            } else {
                console.log("🚨 ユーザーは未認証");
                if (noAuthRedirect) {
                    document.body.classList.remove("loading");
                    window.location.href = noAuthRedirect;
                    return ;
                }
            }
        } else {
            console.error("🚨 認証チェックに失敗 (JWT 失効の可能性あり)", response.status);
            console.log(response.status);

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            if (noAuthRedirect) {
                document.body.classList.remove("loading");
                window.location.href = noAuthRedirect;
                return ;
            }
        }
    } catch (error) {
        console.error("🚨 認証リクエスト中にエラー:", error);
        document.body.classList.remove("loading");
    }
    console.log("stay here maybe?")
    document.getElementById("loading-screen").style.display = "none";
    document.body.classList.remove("loading");
}
