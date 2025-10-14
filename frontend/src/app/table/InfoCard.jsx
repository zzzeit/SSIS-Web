"use client";
import './InfoCard.css'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import { useEffect, useState } from 'react';

export default function InfoCard({ table_name='', visibility, headers = [], valueFuncs = [], refreshFunc }) {
    const [canEdit, setCanEdit] = useState(false);
    const [inputValues, setInputValues] = useState([]);

    const deleteFunc = async () => {
        const oldCode = valueFuncs[0]?.[0];
        if (!oldCode) return;

        const isConfirm = window.confirm(`Are you sure you want to delete ${oldCode}?`);
        if (isConfirm) {
            const response = await fetch(`http://192.168.1.50:5000/delete/${table_name}/${oldCode}`);
            if (response.ok) {
                refreshFunc();
                visibilityFunc();
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occurred. STATUS ${response.status}`);
            }
        }
    }

    const visibilityFunc = () => {
        visibility[1](false);
        setCanEdit(false);
        setInputValues([]);
    };

    const submitEditButton = async () => {
        const oldCode = valueFuncs[0]?.[0];
        if (!oldCode) return;

        // 1. Use the whole inputValues array, not just the first two items.
        const newValues = inputValues;

        // 2. Basic validation to ensure no fields are empty.
        if (newValues.some(val => !val || String(val).trim() === '')) {
            window.alert("All fields must be filled out before submitting.");
            return;
        }

        // 3. Dynamically create the URL path from all the new values.
        const newValuesPath = newValues.join('/');

        // 4. Make the confirmation message more generic.
        const isConfirm = window.confirm(`Are you sure you want to save these changes for item ${oldCode}?`);
        if (isConfirm) {
            // 5. Construct the final URL dynamically.
            const url = `http://192.168.1.50:5000/edit/${table_name}/${oldCode}/${newValuesPath}`;
            console.log("Submitting edit request to:", url);

            const response = await fetch(url);
            if (response.ok) {
                refreshFunc();
                visibilityFunc();
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occurred. STATUS ${response.status}`);
            }
        }
    };

    // 2. Update the effect to populate the inputValues array from the prop
    useEffect(() => {
        // Ensure valueFuncs and its first element exist before setting state
        if (valueFuncs.length > 0 && valueFuncs[0]) {
            setInputValues(valueFuncs[0]);
        }
    }, [valueFuncs]); // Depend on the whole array

    if (!visibility[0] || !valueFuncs[0] || valueFuncs[0].length === 0) {
        return null;
    }

    // 3. Helper function to update a specific input value in the array
    const handleInputChange = (index, value) => {
        const newValues = [...inputValues];
        newValues[index] = value;
        setInputValues(newValues);
    };

    return (
        <>
            <div className="bg-pop-up" onClick={visibilityFunc} />

            <div className="pop-up">
                <div className='header-pop-up'>
                    <HeaderButton onClick={visibilityFunc} style={{ borderTopRightRadius: '10px', width: '45px' }}>
                        <Image src='/close.svg' alt='Close' width={28} height={28} style={{ filter: 'var(--svg-inverse)' }} />
                    </HeaderButton>
                    <HeaderButton onClick={deleteFunc} style={{ width: '45px' }}>
                        <Image src={'/trash.svg'} alt='Trash' width={28} height={28} style={{ filter: 'var(--svg-inverse)' }} />
                    </HeaderButton>
                    <HeaderButton onClick={() => {
                        // Reset inputs to original values when toggling edit mode
                        setInputValues(valueFuncs[0]);
                        setCanEdit(!canEdit);
                    }} style={{ width: '45px' }}>
                        <Image src={'/edit.svg'} alt='Edit' width={28} height={28} style={{ filter: 'var(--svg-inverse)' }} />
                    </HeaderButton>
                </div>

                <InfoCardDatas
                    headers={headers}
                    inputValues={inputValues}
                    handleInputChange={handleInputChange}
                    canEdit={canEdit}
                    submitButtonFunc={submitEditButton}
                />
            </div>
        </>
    );
}

// 4. Make InfoCardDatas dynamic by mapping over the values
function InfoCardDatas({ headers, inputValues, handleInputChange, canEdit, submitButtonFunc }) {
    return (
        <>
            <div className='info-card-datas'>
                {inputValues.map((value, index) => (
                    <InfoCardData
                        key={index}
                        text={`${headers[index] || `Field ${index + 1}`}: `}
                        inputValue={value}
                        setInputFuncs={(newValue) => handleInputChange(index, newValue)}
                        canEdit={canEdit}
                    />
                ))}
            </div>

            {canEdit && <button onClick={submitButtonFunc} className='submit-button'>Done</button>}
        </>
    );
}

function InfoCardData({text='Label: ', inputValue='None', setInputFuncs, canEdit}) {
    let classVar = 'info-card-data';
    if (canEdit) {
        classVar = 'info-card-data-editable';
    }
    return (
        <>
            <div className={classVar}>
                <label>{text}</label>
                <input value={inputValue || ''} onChange={(e) => { setInputFuncs(e.target.value) }} readOnly={!canEdit} />
            </div>
        </>
    );
}