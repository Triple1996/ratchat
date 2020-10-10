import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessageLoc = document.getElementById("chat-input");
    let newMessage = newMessageLoc.value;
    
    if (!/^\s*$/.test(newMessage)) { 
        Socket.emit('new message input', {
            'message': newMessage,
        });
       console.log('Sent the message ' + newMessage + ' to server!'); 
    }
    else {
        
        alert("Text field cannot be empty");
    }
    
    newMessageLoc.value = ''
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
