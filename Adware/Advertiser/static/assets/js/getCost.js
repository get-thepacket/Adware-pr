function cost($this) {

    var id = $this.attr("id");
    var no = id.split("-")[1];
    var cardid = "card"+no;
    console.log(cardid);
    var element = document.getElementById(cardid);
    console.log(element);
    var address = "/scr/get-cost?id="+no;
    $.ajax({
        method: "GET",
        url: address,
        success: function (response) {
            console.log(response);
            element.innerHTML = "Rs." + response;
            document.getElementById(id).value="refresh!!";
            document.getElementById(id).innerHTML="refresh!!";
        }
    });

}