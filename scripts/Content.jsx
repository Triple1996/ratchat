import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('messages received', (data) => {
                console.log("Received messages from server: " + data['allMessages']);
                setMessages(data['allMessages']);
            })
        });
    }
    
    getNewAddresses();

    return (
        <div id="interface">
            <h1>Ratchat</h1>
                <div id='chat-container'>
                    {messages.map((address, index) =>
                        <ul key={index} className="chat-items">{address}</ul>)}
                </div>
            <Button />
        </div>
    );
}
