import { Socket } from './Socket';
import React from 'react';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';


const responseGoogle = (response) => {
  console.log(response);
}
 

function handleSubmit(response) {
    console.log(response);
    let name = response.nt.Ad;
    let email = response.nt.Wt;
    let profilePicURL = response.nt.JJ;

    Socket.emit('new google user', {
        'name': name,
        'email': email,
        'picture': profilePicURL
    });
    console.log('logged in with email ' + email + '!');
    document.getElementById("chat-input").disabled = false;
    document.getElementById("submit").disabled = false;
}

export function GoogleButton() {
    return <GoogleLogin
        clientId="174343683808-a8qlre1saob9enalirddvbkmi4m8al43.apps.googleusercontent.com"
        buttonText="Login to join the chat!"
        onSuccess={handleSubmit}
        onFailure={responseGoogle}
        cookiePolicy={'single_host_origin'}
      />;

}
