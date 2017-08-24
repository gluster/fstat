showSnackBar = function(text, timeout=null) {
  var snackbar = document.getElementById("snackbar");
  snackbar.innerText = text;
  snackbar.className = "show";
  if (timeout) {
    setTimeout(function(){
      snackbar.className = snackbar.className.replace("show", "")
    }, timeout);
  }
};

hideSnackBar = function() {
  var snackbar = document.getElementById("snackbar");
  snackbar.className = snackbar.className.replace("show", "")
};
