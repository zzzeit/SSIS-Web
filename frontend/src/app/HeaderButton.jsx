import './HeaderButton.css'
import Link from 'next/link'

function HeaderButton({ children, myLink, onClick, style }) {
    if (myLink) {
        return (
            <Link href={myLink} className='header-button' style={style}>
                {children}
            </Link>
        );        
    }

    return (
        <button onClick={onClick} className='header-button' style={style}>
            {children}
        </button>
    );        

}

export default HeaderButton;