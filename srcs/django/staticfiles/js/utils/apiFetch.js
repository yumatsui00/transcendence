import { globalUserInfo } from "./userInfo.js";

export async function handleLogout() {
    const access_token = localStorage.getItem("access_token");

    if (!access_token) {
        console.warn("🚨 No access token found. Redirecting to login page...");
		localStorage.removeItem("access_token");
		localStorage.removeItem("refresh_token");
<<<<<<< HEAD
        window.location.href = "../../";
=======
		localStorage.removeItem("user_info");
		globalUserInfo = null;

        window.location.href = "https://yumatsui.42.fr/";
>>>>>>> main
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
	if (access_token) {
		options.headers["Authorization"] = `Bearer ${access_token}`;
	}
	options.headers["Content-Type"] = "application/json";

	console.log("🔍 Sending API Request:", url);
    console.log("🔍 Headers:", options.headers);

    let response;
    try {
        response = await fetch(url, options);
        if (response.status === 401 && refresh_token) {
			// refreshtokenがあるのに失敗→accesstoken期限切れの可能性
            console.warn("🔄 access token has expired. Trying refresh token...");
            const refreshResponse = await fetch("https://yumatsui.42.fr/authenticator/refresh/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh: refresh_token })
            });
            if (refreshResponse.ok) {
                const refreshData = await refreshResponse.json();
                // ✅ 新しいアクセストークンが取得できた場合のみ保存
                if (refreshData.access) {
                    console.log("✅ Got a new access token, retrying request...");
                    localStorage.setItem("access_token", refreshData.access);
                    options.headers["Authorization"] = `Bearer ${refreshData.access}`;
                    // ✅ もう一度 API リクエストを実行
                    response = await fetch(url, options);
                } else {
                    console.error("🚨 Failed to get new access token, logging out...");
                    handleLogout();
                    return response;
                }
            } else {
				// refreshtokenに問題あり
                console.error("🚨 Refresh token expired or invalid. Logging out...");
                handleLogout();
                return response;
            }
        }
        // ✅ 401 以外のレスポンスはそのまま返す
        if (!response.ok) {
            console.error(`🚨 API Error: ${response.status} ${response.statusText}`);
        }

<<<<<<< HEAD
		const refreshResponse = await fetch("../authenticator/refresh/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ refresh: refresh_token })
		});

		if (refreshResponse.ok) {
			const refreshData = await refreshResponse.json();

			// ✅ 新しいアクセストークンが取得できた場合のみ保存
			if (refreshData.access) {
				console.log("✅ Got a new access token, retrying request...");

				localStorage.setItem("access_token", refreshData.access);
				options.headers["Authorization"] = `Bearer ${refreshData.access}`;

				// ✅ もう一度 API リクエストを実行
				response = await fetch(url, options);
			} else {
				console.error("🚨 Failed to get new access token, logging out...");
				handleLogout();
				return response;
			}
		} else {
			console.error("🚨 Refresh token expired or invalid. Logging out...");
			handleLogout();
			return response;
		}
	} else {
		console.log("成功したってこと")
	}
	// ✅ 401 以外のレスポンスはそのまま返す
	return response;
=======
        return response;
    } catch (error) {
        console.error("🚨 API request failed:", error);
        return new Response(JSON.stringify({ error: "Network error" }), { status: 500 });
    }
>>>>>>> main
}
