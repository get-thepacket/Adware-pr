function copy($this) {

    var id = $this.attr("id");
    console.log(id)
    var clipboard = new ClipboardJS(".copy-button", {container: document.getElementById(id)});


  clipboard.on('success', function(e) {
    console.log('success');


  });

}