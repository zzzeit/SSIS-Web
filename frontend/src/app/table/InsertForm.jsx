"use client";
import './InsertForm.css'
import './InfoCard'
import AvatarPicker from '@/components/AvatarPicker/AvatarPicker';

export default function InsertForm({ insert_form_name="Insert Form", fields=[["Field_1: ", null, null], ["Field_2: ", null, null], ["Field_3: ", null]], submitFunc, avatarUpdate }) {

    return (
        <>
            <div className='insert'>
                <div className='insert-header'>
                    <label>{insert_form_name}</label>
                </div>
                <div className='insert-inputs'>
                    {insert_form_name === "Insert Student" ? <AvatarPicker avatarUpdate={avatarUpdate} /> : null}
                    {fields.map((f) => (
                        <div key={f[0]}>
                            <label>{f[0]}</label>
                            <input value={f[1]} onChange={(e) => f[2](e.target.value)}/>
                        </div>
                    ))}

                    <button onClick={() => { submitFunc(); }}>Done</button>
                </div>
            </div>
        </>
    )
}