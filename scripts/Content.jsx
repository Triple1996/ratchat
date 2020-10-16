import * as React from 'react';

import { InputField } from './InputField';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content() {
    const [messages, setMessages] = React.useState([]);
    const [userCount, setUserCount] = React.useState(0);
    
    React.useEffect(() => {
        
        Socket.on('messages received', (data) => {
            console.log("Received messages from server: " + data['allMessages']);
            setMessages(data['allMessages'].reverse());
        })
        
        Socket.on('updateUsers', (data) => {
            setUserCount(data['user_count'])
        })
        
    });
    console.log("picture: " + messages);
    return (
        <div id="interface">
            <h1 id="title">Ratchat</h1>
                <div id="user-count">
                    <span>User count: {userCount}</span>
                </div>
                <div id='chat-container'>
                    <div id='messages-wrapper'>
                        {messages.map((message, index) =>
                            <ul className="chat-items" key={index}>{message[0]}</ul> )}
                    </div>
                    <div id='pics-wrapper'>
                        {messages.map((pics, index) =>
                            <ul className="pictures" key={index}><img src = "{{pics[2]}}" /></ul> )}
                    </div>
                    <div id='users-wrapper'>
                        {messages.map((sign, index) =>
                            <ul className="signatures" key={index}>{sign[1]}</ul>)}
                        <ul id="anchor"></ul>
                    </div>
                </div>
            <InputField />
            <GoogleButton />
        </div>
    );
}
