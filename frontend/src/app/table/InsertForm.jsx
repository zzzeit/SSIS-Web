"use client";
import './InsertForm.css'
import { useState } from 'react';
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import AvatarPicker from '@/components/AvatarPicker/AvatarPicker';

export default function InsertForm({ insert_form_name="Insert Form", fields=[["Field_1: ", null, null], ["Field_2: ", null, null], ["Field_3: ", null]], submitFunc, avatarUpdate }) {
    const [visible, setVisible] = useState(false);

    return (
        <>
            <button type='button' className='add-entry-button' onClick={() => setVisible(true)} title={insert_form_name} aria-label={insert_form_name}>
                +
            </button>

            {visible && (
                <>
                    <div className='bg-pop-up-insert' onClick={() => setVisible(false)} />
                    <div className='pop-up-insert'>
                        <div className='header-pop-up-insert'>
                            <label>{insert_form_name}</label>
                            <HeaderButton onClick={() => setVisible(false)} style={{ borderTopRightRadius: '10px', width: '45px' }}>
                                <Image src='/media/close.svg' alt='Close' width={24} height={24} style={{ filter: 'var(--svg-inverse)' }} />
                            </HeaderButton>
                        </div>
                        <div className='insert-inputs'>
                            {insert_form_name === "Insert Student" ? <AvatarPicker avatarUpdate={avatarUpdate} /> : null}
                            {fields.map((f) => (
                                <div className='insert-input' key={f[0]}>
                                    <label>{f[0]}</label>
                                    {f[0] === "Sex: " ? (
                                        <select value={f[1]} onChange={(e) => f[2](e.target.value)}>
                                            <option value="" disabled style={{display: "none"}}></option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                        </select>
                                    ) : (
                                        <input value={f[1]} onChange={(e) => f[2](e.target.value)} />
                                    )}
                                </div>
                            ))}

                            <button onClick={() => { submitFunc(); }}>Done</button>
                        </div>
                    </div>
                </>
            )}
        </>
    )
}