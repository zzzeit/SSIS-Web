import './HeaderButton.css'
import Link from 'next/link'

function HeaderButton({ text, myLink, style }) {
    return (
        <Link href={myLink} className='header-button' style={style}>
            {text}
        </Link>
    );
}

export default HeaderButton;