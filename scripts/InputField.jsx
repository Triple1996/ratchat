import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newMessageLoc = document.getElementById("chat-input");
    let newMessage = newMessageLoc.value;
    
    // message is empty
    if (/^\s*$/.test(newMessage)) { 
        alert("Text field cannot be empty");
        newMessageLoc.value = ''
    }
    else if (newMessage.length > 240) {
        alert("Message cannot exceed 240 characters.")
    }
    else if (newMessage.trim().substr(0,2) == "~/"){
        alert("Only the bot may start lines with '~/'");
        newMessageLoc.value = ''
    }
    else{
        Socket.emit('new message input', {
            'message': newMessage,
        });
        console.log('Sent the message ' + newMessage + ' to server!'); 
        newMessageLoc.value = ''
    }
    
    event.preventDefault();
}

export function InputField() {
    React.useEffect(() => {
        document.getElementById("chat-input").disabled = true;
        document.getElementById("submit").disabled = true;
    }, []);
    
    return (
        <div id="input-ui">
            <form onSubmit={handleSubmit}>
                <input id="chat-input" placeholder="Enter message" disabled></input>
                <button id="submit" disabled>Send!</button>
            </form>
        </div>
    );
}
