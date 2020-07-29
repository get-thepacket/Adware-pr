function validate($this) {
    var password1 = document.getElementById('id_password1');
    var password2 = document.getElementById('id_password2');
    var email =document.getElementById('id_email');
    var notification = document.getElementById("validate-data");

    if( ! (password1.value || password2.value || email.value))
    {
        console.log("Fill all compulsory fields");
        notification.innerHTML="Fill all fields";
        return false;
    }

    if(password1.value == password2.value){
        console.log("Passwords Matched");
        console.log(/^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$/.test(password1.value))
        if(/^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}.*$/.test(password1.value)){
            console.log("Password Strong");
            $("#form-button").trigger('click');
        }
        else{
            console.log("Password is week");
            notification.innerHTML="Password is week";
        }
    }
    else{
        notification.innerHTML="Password is Week";
        console.log("Password value don't match")
    }
}