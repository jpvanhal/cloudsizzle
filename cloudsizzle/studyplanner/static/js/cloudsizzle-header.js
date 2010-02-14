function addfriend(uri, node) {
    $.ajax({
        url: uri,
        type: "POST",
        beforeSend: function(XMLHttpRequest) {
            document.getElementById(node).innerHTML = "processing";
            document.getElementById(node).onclick = "";
        },
        success: function(data, textStatus, XMLHttpRequest) {
            document.getElementById(node).innerHTML = "friend request sent";
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            document.getElementById(node).innerHTML = textStatus;
        }
    });
}
