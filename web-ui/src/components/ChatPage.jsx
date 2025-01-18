// src/components/Page.js
import React from 'react';
import HamburgerMenu from './HamburgerMenu';
import {Chat, InputBlock} from './Chat';
import getUser from '../User';

class ChatPage extends React.Component {

    constructor({props})
    {
        super(props);
        this.state = {user:null, chats:[], chat : {messages:[{authon:"user", text:"test",}]}}
    }

    async componentDidMount()
    {
        let user = await getUser();
        this.setState({...this.state, user:user});
    }

    createChat()
    {

    }

    render() {
        return (
            <>
            <div className="page">
                <HamburgerMenu onCreate={this.createChat.bind(this)} chats={["chat_1", "chat_2"]} />
                { (this.state.chat != null) ?  (
                    <div className="main-chat-window"> 
                        <Chat messages={this.state.chat.messages} />
                        <InputBlock /> 
                    </div>) : (<> <p>Select or create chat to chat</p> <button onClick={this.createChat.bind(this)}>New chat</button> </>)
                }
                
            </div>
            </>
        );
    }
}

export default ChatPage;
