import { getDeviceName } from "/static/js/utils/getDeviceName.js";
import { translations_format } from "/static/js/utils/translations";


export function signupflow(username, email, password, is_2fa_enabled, language) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("language", language);
    formData.append("password", password);
    formData.append("is_2fa_enabled", is_2fa_enabled);

    try {
        if (!username || username.length > 10) {
            alert("ユーザーネームは１〜１０文字以内で入力してください")
        }
        //重複チェック
        console.log("Sending data:", Object.fromEntries(formData.entries())); // 🔍 送信データを確認
        const response = await fetch("https://yumatsui.42.fr/user/signup/", {
            method: "POST",
            body: formData
        });

        const data = await response.json()
        messageBox.textContent = data.message;
        if (response.ok) {
            //password有効性チェック
            //userid発行＆
        }
    } catch (error) {
        console.error("Error: ", error);
        message.textContent = "SignUp Failed";
    }
}