import Link from 'next/link'
import './HeaderDropdownMenu.css'

function HeaderDropdownMenu({ text, myLink, style }) {
    return (
        <>
            <div className='menu'>
                <button> {text} </button>
                <div className='content'>
                    <Link href={myLink} className='header-button' style={style}>
                        College
                    </Link>
                    <Link href={myLink} className='header-button' style={style}>
                        Program
                    </Link>
                    <Link href={myLink} className='header-button last-menu-item' style={style}>
                        Students
                    </Link>
                </div>
                
            </div>
        </>
    )
}

export default HeaderDropdownMenu;