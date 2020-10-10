import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById("chat-input");

    if (newMessage.value != "") { 
        Socket.emit('new message input', {
            'message': newMessage.value,
        });
       console.log('Sent the message ' + newMessage.value + ' to server!'); 
    }
    else {
        alert("Text field cannot be empty");
    }
    
    newMessage.value = ''
    
    event.preventDefault();
}

export function InputField() {
    return (
        <div id="input-ui">
            <form onSubmit={handleSubmit}>
                <input id="chat-input" placeholder="Enter message"></input>
                <button id="submit">Send!</button>
            </form>
        </div>
    );
}
