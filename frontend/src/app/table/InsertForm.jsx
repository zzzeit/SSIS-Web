"use client";
import './InsertForm.css'
import './InfoCard'

export default function InsertForm({ insert_form_name="Insert Form", fields=[["Field_1: ", null, null], ["Field_2: ", null, null], ["Field_3: ", null]], functions=[] }) {
    const submitButton = async () => {
        await functions[1]();

        await new Promise(resolve => setTimeout(resolve, 100));

        functions[0]();
        functions[2]();
    }
    return (
        <>
            <div className='insert'>
                <div className='insert-header'>
                    <label>{insert_form_name}</label>
                </div>
                <div className='insert-inputs'>

                    {fields.map((f) => (
                        <div key={f}>
                            <label>{f[0]}</label>
                            <input value={f[1]} onChange={(e) => f[2](e.target.value)}/>
                        </div>
                    ))}

                    <button onClick={submitButton}>Done</button>
                </div>
            </div>
        </>
    )
}