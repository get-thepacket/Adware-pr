function copy($this) {

    var id = $this.attr("id");
    var classid = $this.attr("class");
    var first = classid.split(" ")[0];
    //console.log(id,classid,first);
    var clipboard = new ClipboardJS('.'+first, {container: document.getElementById(id)});

    var element = document.getElementById(id);
    clipboard.on('success', function(e) {
        element.value="copied!!";
        element.innerHTML="copied!!";
        setTimeout(function() {
            document.getElementById(id).value="copy";
            document.getElementById(id).innerHTML="copy";
    }, 1000);
  });

}