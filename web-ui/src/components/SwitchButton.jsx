
export default function SwitchButton({toggle, onClick, children})
{

    return (<button className={toggle?"toggle-button-on": "toggle-button-off"} onClick={onClick}>{children}</button>)
}