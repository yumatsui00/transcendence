document.addEventListener("DOMContentLoaded", () => {
	const params = new URLSearchParams(window.location.search);
	const email = params.get("email");
	const qrCodeUrl = params.get("qr_code_url");

	document.getElementById("qr-ok-btn").addEventListener("click", () => {
		// ✅ email と qr_code_url を URL パラメータとして渡す
<<<<<<< HEAD
		window.location.href = `../authenticator/otp/?email=${encodeURIComponent(email)}&qr_code_url=${encodeURIComponent(qrCodeUrl)}`;
=======
		window.location.href = `https://yumatsui.42.fr/authenticator/otp/?email=${encodeURIComponent(email)}}`;
>>>>>>> main
	});
});