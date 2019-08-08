function showSignInBtn(setVisible) {
    var login_btn = document.getElementById("login");
    var logout_btn = document.getElementById("logout");
    if (setVisible) {
        login_btn.style.display = "block";
        logout_btn.style.display = "none";
    } else {
        login_btn.style.display = "none";
        logout_btn.style.display = "block";
    }
}
    //if(setVisible) {
      //  $('.sign-in').css('display', 'block');
        //$('.sign-out').css('display', 'none');
    //}
    //else {
      //  $('.sign-in').css('display', 'none');
        //$('.sign-out').css('display', 'block');
    //}
//}

