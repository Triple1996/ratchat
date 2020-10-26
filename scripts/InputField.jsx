import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
  const newMessageLoc = document.getElementById('chat-input');
  const newMessage = newMessageLoc.value;

  // message is empty
  if (/^\s*$/.test(newMessage)) {
    document.getElementById('response-field').innerHTML = 'Text field cannot be empty';
    newMessageLoc.value = '';
  } else if (newMessage.length > 200) {
    document.getElementById('response-field').innerHTML = 'Message cannot exceed 200 characters.';
  } else if (newMessage.trim().substr(0, 2) === '~/') {
    document.getElementById('response-field').innerHTML = "Only the bot may start lines with '~/'";
    newMessageLoc.value = '';
  } else {
    document.getElementById('response-field').innerHTML = '';
    Socket.emit('new message input', {
      message: newMessage,
    });
    newMessageLoc.value = '';
  }

  event.preventDefault();
}

export function InputField() {
  React.useEffect(() => {
    document.getElementById('chat-input').disabled = true;
    document.getElementById('submit').disabled = true;
  }, []);

  return (
    <div id="input-ui">
      <form onSubmit={handleSubmit}>
        <input id="chat-input" placeholder="Enter message" disabled />
        <button id="submit" type="button" disabled>Send!</button>
      </form>
    </div>
  );
}
