import { getUserInfo } from "/static/js/utils/getUserInfo.js";
import { checkAuth } from "/static/js/utils/checkAuth.js";
import { translations_format } from "/static/js/utils/translations.js"

// checkAuth(null, "https://yumatsui.42.fr/");

// intに変換
const lang = parseInt(localStorage.getItem("language"), 10) || 0;
const translations = translations_format[lang];


document.getElementById("title").textContent = translations.gamemenu; // ゲームメニュータイトル
document.getElementById("cpu-battle-btn").textContent = translations.cpumatch;
document.getElementById("random-match-btn").textContent = translations.randommatch;
document.getElementById("friend-battle-btn").textContent = translations.friendmatch;
document.getElementById("settings-btn").textContent = translations.setting;
document.getElementById("friend-list-btn").textContent = translations.friendlist;

// ボタンのクリック処理
function handleClick(page) {
    let url = '';
    switch (page) {
        case 'CPU Battle':
            url = '/cpu-battle/';
            break;
        case 'Random Match':
            url = '/matchmaking/';
            break;
        case 'Friend Battle':
            url = '/friend-battle/';
            break;
        case 'Settings':
            url = '/pages/setting/';
            break;
        case 'Friend List':
            url = '/friend-list/';
            break;
        default:
            console.error('Unknown page:', page);
            return;
    }
    window.location.href = url;
}

// グローバルに関数を登録（HTMLの `onclick` を動作させるため）
window.handleClick = handleClick;
