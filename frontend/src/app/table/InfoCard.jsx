"use client";
import './InfoCard.css'
import '../HeaderButton'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import InfoCardData from './InfoCardData';

export default function InfoCard({visibility, values}) {

    const deleteFunc = async () => {
        const isConfirm = window.confirm(`Are you sure you want to delete ${values[0]}?`);

        if (isConfirm) {
            const d = await fetch(`http://localhost:5000/delete/college/${values[0]}`);
            console.log(d);
        }
    }

    if (!visibility[0]) {
        return null;
    }

    return (
        <>
            <div className="bg-pop-up" onClick={() => {visibility[1](false)}} />

            <div className="pop-up">
                <div className='header-pop-up'>
                    <HeaderButton onClick={() => {visibility[1](false)}} style={{borderTopRightRadius: '10px', width: '45px'}}>
                        <Image src='/close.svg' alt='Close' width={28} height={28} className='invert' />
                    </HeaderButton>
                    <HeaderButton onClick={() => {deleteFunc();}} style={{width: '45px'}}>
                        <Image src={'/trash.svg'} alt='Trash' width={28} height={28} className='invert' />
                    </HeaderButton>
                    <HeaderButton style={{width: '45px'}}>
                        <Image src={'/edit.svg'} alt='Edit' width={28} height={28} className='invert' />
                    </HeaderButton>

                </div>

                <InfoCardData text='Code: ' value={values[0]} />
                <InfoCardData text='Name: ' value={values[1]} />
                
            </div>
        </>
    );
}