<%inherit file="/html5.mako" />
<head>
    <title>QuickNote - Edit</title>
    <link rel="stylesheet" type="text/css" href="/static/css/editor.css" />
    <script language="javascript" type="text/javascript" src="/static/js/jquery-1.7.1.js"></script>
    <script language="javascript" type="text/javascript" src="/static/js/editor.js"></script>
</head>
<body>
<form id="editform" action=${escattr(urlfor("document.edit_do",id_=id_))} method="POST">
    <div id="actionbar">
        <input type="submit" name="action" value="Save" tabindex="2">
        <input type="submit" id="deletebutton" name="action" value="Delete" tabindex="3">
    </div>
    <div id="editor">
        <textarea id="content" name="content" tabindex="1">${escape(content)}</textarea>
    </div>
</form>
</body>
