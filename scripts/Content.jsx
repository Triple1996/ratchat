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
        
        console.log(document.getElementsByClassName("chat-items"))
        console.log(messages)
        renderHTML()
    });
    
    Socket.on('connect', (data) => {
            renderHTML()
    })
    
    function renderHTML() {
        var chats = messages.reverse();
        console.log("renderHTML(), new messages: " + messages);
        for (var i = 0; i < messages.length; i++) {
                document.getElementsByClassName("chat-items")[i].innerHTML = chats[i][0];
            }
    }
    
    return (
        <div id="interface">
            <h1 id="title">Ratchat</h1>
                <div id="user-count">
                    <span>User count: {userCount}</span>
                </div>
                <div id='chat-container'>
                    <div id='messages-wrapper'>
                        {messages.map((message, index) =>
                            <ul className="chat-items" key={index}></ul> )}
                    </div>
                    <div id='pics-wrapper'>
                        {messages.map((pics, index) =>
                            <ul key={index}><img src={pics[2]} className="pictures" /></ul> )}
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
