export function handleLogout() {
	localStorage.removeItem("access_token");
	localStorage.removeItem("refresh_token");
	//TODO もしbackendで必要なものがあればここで
	window.location.href = "https://yumatsui.42.fr/"
}