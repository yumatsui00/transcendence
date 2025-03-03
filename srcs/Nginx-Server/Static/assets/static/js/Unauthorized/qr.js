function getUrlParams() {
    const pathSegments = window.location.pathname.split('/');  // `/` で分割
    const userid = pathSegments[2];  // `/get_qr/{userid}/{qr_url}` の `userid`
    const qrUrlEncoded = pathSegments[3];
    return { userid, qrUrlEncoded };
}

const { userid, qrUrlEncoded } = getUrlParams();

// ✅ QRコードを取得し、表示する関数
async function fetchQRCode() {
    try {
        // ✅ QR URL をデコード
        const decodedQrUrl = atob(qrUrlEncoded);  // Base64デコード

        console.log("デコード後のQR URL:", decodedQrUrl);  // デバッグ用ログ

        // ✅ API にリクエストを送る
        const response = await fetch(`https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=${encodeURIComponent(decodedQrUrl)}`, {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // ✅ 画像を `<img>` にセット
        document.getElementById("qrImage").src = response.url;
    } catch (error) {
        console.error("エラー:", error);
    }
}


// ✅ ページ読み込み時に QRコードを取得
window.onload = fetchQRCode;


document.addEventListener("DOMContentLoaded", () => {
	document.getElementById("qr-ok-btn").addEventListener("click", () => {
		// ✅ email と qr_code_url を URL パラメータとして渡す
		window.location.href = `${window.location.origin}/authenticator/otp/?email=${encodeURIComponent(email)}}`;
	});
});