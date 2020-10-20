import * as React from 'react';

import { InputField } from './InputField';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [userCount, setUserCount] = React.useState(0);
    
    React.useEffect(() => {
        Socket.on('messages received', (data) => {
            console.log("Received messages from server.");
            setMessages(data['allMessages'].reverse());
        })
        
        Socket.on('updateUsers', (data) => {
            setUserCount(data['user_count'])
        })
    });

    return (
        <div id="interface">
            <h1 id="title">Ratchat</h1>
                <div id="user-count">
                    <span>Logged in user count: {userCount}</span>
                </div>
                <div id='chat-container'>
                        {messages.map((message, index) =>
                            <ul id='messages-wrapper' key={index}>
                                <div className="chat-items" dangerouslySetInnerHTML={{__html: `${message[0]}` }}></div>
                                <div className ="pic-items"><img src={message[2]} className="pictures" /></div>
                                <div className="signatures">{message[1]}</div>
                            </ul>
                        )}
                </div>
            <InputField />
            <GoogleButton />
        </div>
    );
}
