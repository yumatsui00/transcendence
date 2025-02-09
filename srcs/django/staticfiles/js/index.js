const translations = {
    en: {
        welcome: "Welcome to Our Service",
        signup: "Sign Up",
        login: "Login"
    },
    ja: {
        welcome: "サービスへようこそ",
        signup: "サインアップ",
        login: "ログイン"
    },
    fr: {
        welcome: "Bienvenue sur Notre Service",
        signup: "S'inscrire",
        login: "Se connecter"
    }
};

function updateLanguage(lang) {
    document.getElementById('welcome').textContent = translations[lang].welcome;
    document.getElementById('signup').textContent = translations[lang].signup;
    document.getElementById('login').textContent = translations[lang].login;
}

document.getElementById('language').addEventListener('change', function() {
    updateLanguage(this.value);
});

document.getElementById('signup').addEventListener('click', function() {
    window.location.href = '/signup/'
});

document.getElementById('login').addEventListener('click', function() {
    alert('Login clicked');
});

// Initialize with English
updateLanguage('en');
