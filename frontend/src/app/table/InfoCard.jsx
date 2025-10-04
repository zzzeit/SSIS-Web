"use client";
import './InfoCard.css'
import '../HeaderButton'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import { useState } from 'react';

export default function InfoCard({visibility}) {

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
                    <HeaderButton style={{width: '45px'}}>
                        <Image src={'/trash.svg'} alt='Trash' width={28} height={28} className='invert' />
                    </HeaderButton>
                    <HeaderButton style={{width: '45px'}}>
                        <Image src={'/edit.svg'} alt='Edit' width={28} height={28} className='invert' />
                    </HeaderButton>

                </div>
                
            </div>
        </>
    );
}