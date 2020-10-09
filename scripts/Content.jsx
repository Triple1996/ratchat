import * as React from 'react';

import { InputField } from './InputField';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [users, setUsers] = React.useState(0);
    
    React.useEffect(() => {
        
        Socket.on('messages received', (data) => {
            console.log("Received messages from server: " + data['allMessages']);
            setMessages(data['allMessages']);
        })
        
        Socket.on('updateUsers', (data) => {
            setUsers(data['user_count'])
        })
        

        
    });

    return (
        <div id="interface">
            <h1>Ratchat</h1>
                <span>{users}</span>
                <div id='chat-container'>
                    {messages.map((address, index) =>
                        <ul className="chat-items" key={index}>{address}</ul>)}
                </div>
            <InputField />
        </div>
    );
}
