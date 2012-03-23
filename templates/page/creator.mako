<%inherit file="/html5.mako" />
<head>
    <title>QuickNote - Create</title>
    <link rel="stylesheet" type="text/css" href="/static/css/editor.css" />
    <script language="javascript" type="text/javascript" src="/static/js/jquery-1.7.1.js"></script>
    <script language="javascript" type="text/javascript" src="/static/js/editor.js"></script>
</head>
<body>
<form action=${escattr(urlfor("document.create_do"))} method="POST">
    <div id="actionbar">
        <input type="submit" value="Save" tabindex="2">
    </div>
    <div id="editor">
        <textarea id="content" name="content" tabindex="1"></textarea>
    </div>
</form>
</body>
