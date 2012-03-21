$(function(){
    var refresh = function(){
        var draw = function(data){
            var resdiv = $("<div>");
            resdiv.append(
                $("<a>").addClass("createnote")
                .attr("href", "/create")
                .text("Create new")
            );
            data.forEach(function(entry){
                resdiv.append(
                    $("<a>").addClass("note")
                    .attr("href", "/note/" + encodeURIComponent(entry.id))
                    .text(entry.text)
                );
            });
            $("#results").empty().append(resdiv);
        }
        var drawsearch = function(data){
            var resdiv = $("<div>");
            data.forEach(function(entry){
                resdiv.append(
                    $("<a>").addClass("note")
                    .attr("href", "/note/" + encodeURIComponent(entry.id))
                    .text(entry.text)
                );
            });
            $("#results").empty().append(resdiv);
        }

        var query = $("#filtertext").val();
        if(query.trim() === "")
            $.getJSON("/sys/latest", draw);
        else
            $.getJSON("/sys/search", {q: query}, drawsearch);
    }
    refresh();
    $("#filtertext").on("keyup", refresh);
});
