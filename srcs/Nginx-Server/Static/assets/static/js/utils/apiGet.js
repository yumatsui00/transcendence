export async function apiGet(url) {
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");


    if (!access_token || !refresh_token) {
        console.error("no token found")
        window.location.href = `https://localhost:8443/`
    }
    let options = {}
    options.headers["Authorization"] = `Bearer ${access_token}`;


    try {
        let response = await fetch(url, options);

        // ✅ 401 (Unauthorized) ならアクセストークンの期限切れの可能性
        if (response.status === 401 && refresh_token) {
            console.warn("🔄 Access token expired. Trying refresh token...");

            const refreshResponse = await fetch("https://localhost:8443/authenticator/refresh/", {
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