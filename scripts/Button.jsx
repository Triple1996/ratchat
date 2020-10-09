import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessage = document.getElementById("chat-input");
    Socket.emit('new message input', {
        'message': newMessage.value,
    });
    
    console.log('Sent the message ' + newMessage.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
}

export function Button() {
    return (
        <div id="input-ui">
            <form onSubmit={handleSubmit}>
                <input id="chat-input" placeholder=""></input>
                <button id="submit">Send!</button>
            </form>
        </div>
    );
}
