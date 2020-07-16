function ajax($this) {
    var id = $this.attr("id");
    console.log(id);
    var address = "/adv/wait?id="+id;

    $.ajax({
        method: "GET",
        url: address,
        success: function (response) {
            console.log(response);
            if(response=="success")
            {
                $('#NotifySuc').modal('show');
            }
            if(response=="error")
            {
                $('#NotifyErr').modal('show');
            }
            if(response=="already")
            {
                $('#NotifyAlr').modal('show');
            }
        }
    });
}