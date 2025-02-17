import { globalUserInfo } from "./userInfo.js";

export async function handleLogout() {
    const access_token = localStorage.getItem("access_token");

    if (!access_token) {
        console.warn("🚨 No access token found. Redirecting to login page...");
		localStorage.removeItem("access_token");
		localStorage.removeItem("refresh_token");
		localStorage.removeItem("user_info");
        localStorage.removeItem("language");
		globalUserInfo = null;

        window.location.href = "https://yumatsui.42.fr/";
        return;
    }

    try {
        const response = await fetch("../authenticator/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,  // JWTを送信
            },
        });

        if (response.ok) {
            console.log("✅ Successfully logged out and deactivated user.");
        } else {
            console.error(`🚨 Logout API request failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error("🚨 Error during logout request:", error);
    }

    // 🔹 ローカルストレージのトークン削除
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    // 🔹 ログアウト後にログインページへリダイレクト
    window.location.href = "../../";
}




export async function apiFetch(url, options = {}) {
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");

    if (!options.headers) {
        options.headers = {};
    }

    // ✅ `FormData` の場合は `Content-Type` を自動設定しない
    if (!(options.body instanceof FormData)) {
        options.headers["Content-Type"] = "application/json";
    }

    if (access_token) {
        options.headers["Authorization"] = `Bearer ${access_token}`;
    }

    console.log("🔍 Sending API Request:", url);
    console.log("🔍 Headers:", options.headers);

    try {
        let response = await fetch(url, options);

        // ✅ 401 (Unauthorized) ならアクセストークンの期限切れの可能性
        if (response.status === 401 && refresh_token) {
            console.warn("🔄 Access token expired. Trying refresh token...");

            const refreshResponse = await fetch("https://yumatsui.42.fr/authenticator/refresh/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh: refresh_token })
            });

            if (refreshResponse.ok) {
                const refreshData = await refreshResponse.json();
                if (refreshData.access) {
                    console.log("✅ Got a new access token, retrying request...");
                    localStorage.setItem("access_token", refreshData.access);
                    options.headers["Authorization"] = `Bearer ${refreshData.access}`;

                    // ✅ アクセストークン更新後にもう一度 API リクエスト
                    response = await fetch(url, options);
                } else {
                    console.error("🚨 Failed to get new access token, logging out...");
                    handleLogoutSafely();
                    return response;
                }
            } else {
                console.error("🚨 Refresh token expired or invalid. Logging out...");
                handleLogoutSafely();
                return response;
            }
        }

        if (!response.ok) {
            console.error(`🚨 API Error: ${response.status} ${response.statusText}`);
        }

        return response;
    } catch (error) {
        console.error("🚨 API request failed:", error);
        return new Response(JSON.stringify({ error: "Network error" }), { status: 500 });
    }
}

// ✅ `handleLogout()` のエラー防止
function handleLogoutSafely() {
    if (typeof handleLogout === "function") {
        handleLogout();
    } else {
        console.warn("⚠️ handleLogout() is not defined. Skipping logout.");
    }
}
