import React, { useState } from 'react';
import SwitchButton from './SwitchButton';

export function Chat({messages}) {
    return (
            <div className="chat-messages">
                {messages.map(message => {
                    return (<p key={message.key} className={message.author === 'user'?"user-message":"model-message"}>{message.text}</p>)
                })}
            </div>
    );
}

export function InputBlock({onChange, onSend})
{
    let [useRag, setRag] = useState(false);

    return ( <div className="input-block">
        <input type="text" onChange={onChange} placeholder="Type a message..." />
        <div style={{display:'flex', justifyContent:"space-between"}}>
            <SwitchButton toggle={useRag} onClick={e => setRag(!useRag)}>
                {useRag ? 'Using RAG' : 'Use RAG'}
            </SwitchButton>
            <button onClick={onSend}>send</button>
        </div>
    </div>);

}

export default Chat;
