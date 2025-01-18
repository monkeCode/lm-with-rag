import React from 'react';
import {useNavigate} from "react-router-dom";

function HamburgerMenu({chats, onCreate})
{
    let navigate = useNavigate();
    return (
        <div className="hamburger-menu">
            <div style={{display:"flex", flexDirection:"row", alignItems:"baseline", justifyContent:"space-between"}}>
            <h2>Chats</h2>
            <button onClick={onCreate} className='empty-button'>+</button>
            </div>
            <ul>
                {chats.map(chat => {
                    return (<li key={chat.id} > <button className='empty-button' onClick={e => navigate(`/chat/${chat.id}`)}>
                        {chat}
                        </button>  </li>)
                })}
            </ul>
        </div>
    );
}

export default HamburgerMenu;
