"use client";
import submitCollege from './submitCollege';
import { useRef, useState } from 'react'

export default function InsertCollegeForm(props) {
    const submitFunc = async () => {
        await submitCollege(collegeCode, collegeName);

        await new Promise(resolve => setTimeout(resolve, 500));

        props.fetchFunc();
        clearFields();
    }
    const clearFields = () =>{
        setCollegeCode('');
        setCollegeName('');
    }
    const [collegeCode, setCollegeCode] = useState('');
    const [collegeName, setCollegeName] = useState('');
    return (
        <>
            <div className='insert'>
                <div className='insert-header'>
                    <label>Insert College</label>
                </div>
                <div className='insert-inputs'>
                    <div>
                        <label>Code: </label>
                        <input value={collegeCode} onChange={(e) => setCollegeCode(e.target.value.toUpperCase())}></input>
                    </div>
                    <div>
                        <label>Name: </label>
                        <input value={collegeName} onChange={(e) => setCollegeName(e.target.value)}></input>
                    </div>
                    <button onClick={submitFunc}>Done</button>
                </div>
            </div>
        </>
    )
}