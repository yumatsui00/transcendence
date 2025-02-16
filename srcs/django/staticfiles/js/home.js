import { getUserInfo } from "./utils/getUserInfo.js";
import { checkAuth } from "/static/js/utils/checkAuth.js";

checkAuth(null, "https://yumatsui.42.fr/");


function handleClick(page) {
    let url = '';

    switch (page) {
        case 'CPU Battle':
            url = '/cpu-battle/'; // CPU対戦ページ
            break;
        case 'Random Match':
            url = '/matchmaking/'; // ランダムマッチページ
            break;
        case 'Friend Battle':
            url = '/friend-battle/'; // 友人対戦ページ
            break;
        case 'Settings':
            url = '/home/setting/'; // 設定ページ
            break;
        case 'Friend List':
            url = '/friend-list/'; // 友人一覧ページ
            break;
        default:
            console.error('Unknown page:', page);
            return;
    }

    // ページ遷移
    window.location.href = url;
}

// グローバルに関数を登録（HTMLの `onclick` を動作させるため）
window.handleClick = handleClick;
