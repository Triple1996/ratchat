import * as React from 'react';

import { InputField } from './InputField';
import { Socket } from './Socket';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [signs, setSigns] = React.useState([]);
    const [userCount, setUserCount] = React.useState(0);
    
    React.useEffect(() => {
        
        Socket.on('messages received', (data) => {
            console.log("Received messages from server: " + data['allMessages']);
            setMessages(data['allMessages']);
            setSigns(data['allSigns']);
        })
        
        Socket.on('updateUsers', (data) => {
            setUserCount(data['user_count'])
        })
        
    });

    return (
        <div id="interface">
            <h1>Ratchat</h1>
                <div id="user-count">
                    <span>User count: {userCount}</span>
                </div>
                <div id='chat-container'>
                    <div id='messages-wrapper'>
                        {messages.map((message, index) =>
                            <ul className="chat-items" key={index}>{message}</ul>)}
                    </div>
                    <div id='users-wrapper'>
                        {signs.map((sign, index) =>
                            <ul className="signatures" key={index}>{sign}</ul>)}
                    </div>
                </div>
            <InputField />
        </div>
    );
}
