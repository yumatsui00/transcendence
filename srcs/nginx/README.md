DjangoでHTMLを配信し、NGINXでjsとCSSを配信する理由
NGINXは静的ファイル、Djangoは動的なファイルを配信するのに向いている→パフォーマンス向上

特にvanilla jsの場合、.htmlを動的にすることが多い。
<h1>ようこそ, {{ user.username }} さん!</h1>
こういうの

だから、これがいい？