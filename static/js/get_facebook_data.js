$(document).ready(function() {
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '527044020761840',
            xfbml      : true,
            version    : 'v2.1'
        });

        // login user
        login()

        // if(FB.getSession != null) {
        //     FB.api('/me', function(data) {
        //         alert("Welcome " + data.name + ": Your UID is " + data.id);
        //         user_id = data.id;
        //     });
        // }

        // actual code
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                // the user is logged in and has authenticated your
                // app, and response.authResponse supplies
                // the user's ID, a valid access token, a signed
                // request, and the time the access token 
                // and signed request each expire

                var uid = response.authResponse.userID;
                var accessToken = response.authResponse.accessToken;
                console.log("access token:" + accessToken);
            } else if (response.status === 'not_authorized') {
                console.log("logged in, hasn't authenticated")
                // the user is logged in to Facebook,
                // but has not authenticated your app
            } else {
                // the user isn't logged in to Facebook.
            }
        });
    };


    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

});

// logs in a user!
function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', function(response) {
                console.log('Good to see you, ' + response.name + '.');
                console.log('user id: ' + response.id);
                console.log(response);
                // user_access_token = response.authResponse.accessToken;
                // console.log("user access token:", user_access_token);
                get_posts(response.id);
                //logged in, everything good
            });
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: 'public_profile, user_friends, user_activities, user_status, user_videos'});
}

function get_posts(user_id) {
    FB.api('/me/feed?limit=200', function(response) {
        console.log(response);
    });
}
