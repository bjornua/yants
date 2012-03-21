<%inherit file="/main.mako" />
<%
    response.status_code = 404
%>

<h1>Siden blev ikke fundet</h1>

<p>
    Siden du søgte blev ikke fundet. <a href="javascript:history.go(-1);">Klik
    her for at gå tilbage</a> eller brug menuen for at komme videre.
</p>
