    
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
        <div>
            <h1>Welcome to the Deep Chat!</h1>
                <ol>
                    {messages.map((address, index) =>
                        <li key={index}>{address}</li>)}
                </ol>
            <Button />
        </div>
    );
}
