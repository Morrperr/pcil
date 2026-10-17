"""Build index.html from src/app.html (the same page that runs inside Claude)."""
import os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
src=open('src/app.html',encoding='utf-8').read()
src=src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
title_line='<title>PC-LI</title>\n'
assert src.startswith(title_line); body=src[len(title_line):]
head='''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>PC-LI: המחשב שמתאים לי</title>
<meta name="description" content="PC-LI: בונים מחשב בקלות, משווים מחירים בין חנויות בישראל, ומבינים כל חלק בעברית פשוטה. חינם, בלי פרסומות ובלי עמלות.">
<meta name="theme-color" content="#FF6D00">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="PC-LI">
<meta property="og:title" content="PC-LI: המחשב שמתאים לי">
<meta property="og:description" content="בונים מחשב, משווים מחירים בין חנויות, ומבינים כל חלק בעברית פשוטה. חינם, בלי פרסומות.">
<meta property="og:image" content="icons/icon-512.png">
'''
tail='''
<script>if("serviceWorker" in navigator){ window.addEventListener("load", function(){ navigator.serviceWorker.register("sw.js").catch(function(){}); }); }</script>
</body>
</html>
'''
# split style/head part vs body content: put <link>/<style> into head
i=body.index('</style>')+len('</style>')
out=head+body[:i]+'\n</head>\n<body>\n'+body[i:]+tail
open('index.html','w',encoding='utf-8').write(out)
