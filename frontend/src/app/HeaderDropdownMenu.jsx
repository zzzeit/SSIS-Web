import Link from 'next/link'
import './HeaderDropdownMenu.css'

function HeaderDropdownMenu({ text, myLinks=["/table", "/table", '/table'], style }) {
    return (
        <>
            <div className='menu'>
                <button> {text} </button>
                <div className='content'>
                    <Link href={myLinks[0]} className='header-button' style={style}>
                        College
                    </Link>
                    <Link href={myLinks[1]} className='header-button' style={style}>
                        Program
                    </Link>
                    <Link href={myLinks[2]} className='header-button last-menu-item' style={style}>
                        Students
                    </Link>
                </div>
                
            </div>
        </>
    )
}

export default HeaderDropdownMenu;