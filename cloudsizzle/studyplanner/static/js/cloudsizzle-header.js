function addfriend(url, node) {
    $.post(url);
    document.getElementById(node).innerHTML = "friend request sent";
    document.getElementById(node).onclick = "";
}
