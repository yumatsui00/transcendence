

document.getElementById("signupBtn").addEventListener("click", async function () {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const language = document.getElementById("language").value;
    const color = 0

    if (!username || !email || !password) {
        document.getElementById("message").textContent = "All fields are required";
        return;
    }

    try {
        const response = await fetch("https://yumatsui.42.fr/api/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password, language, color })
        });
        // credentals: include を用いることでjwtの設定等も可能

        const data = await response.json();
        document.getElementById("message").textContent = data.message;

        if (data.success) {
            alert("Signup successful!");
            console.log("🚀 Response:", data);
            // window.location.href = "/login";  // 成功したらログインページへリダイレクト
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("message").textContent = "Signup failed";
    }
});