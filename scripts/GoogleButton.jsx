import React from 'react';
import GoogleLogin from 'react-google-login';
import { Socket } from './Socket';

function handleSubmit(response) {
  const { name } = response.profileObj;
  const { email } = response.profileObj;
  const profilePicURL = response.profileObj.imageUrl;

  Socket.emit('new google user', {
    name,
    email,
    picture: profilePicURL,
  });
  document.getElementById('chat-input').disabled = false;
  document.getElementById('submit').disabled = false;
}

export default function GoogleButton() {
  return (
    <GoogleLogin
      clientId="174343683808-a8qlre1saob9enalirddvbkmi4m8al43.apps.googleusercontent.com"
      buttonText="Login to join the chat!"
      onSuccess={handleSubmit}
      cookiePolicy="single_host_origin"
    />
  );
}
