"use client";
import './InfoCard.css'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import AvatarPicker from '@/components/AvatarPicker/AvatarPicker';
import { useEffect, useState } from 'react';
import { updateFile } from '@/utils/supaClient';

export default function InfoCard({ table_name='', visibility, headers = [], valueFuncs = [], refreshFunc, editDeleteFuncs = [] }) {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const [canEdit, setCanEdit] = useState(false);
    const [inputValues, setInputValues] = useState([]);


    const visibilityFunc = () => {
        visibility[1](false);
        setCanEdit(false);
        setInputValues([]);
    };

    const submitEditButton = () => {
        if (typeof editDeleteFuncs[0] === 'function') {
            editDeleteFuncs[0](valueFuncs, inputValues, refreshFunc, visibilityFunc);
        }
    };

    const deleteFunc = () => {
        if (typeof editDeleteFuncs[1] === 'function') {
            editDeleteFuncs[1](valueFuncs, refreshFunc, visibilityFunc);
        }
    };

    // 2. Update the effect to populate the inputValues array from the prop
    useEffect(() => {
        // Ensure valueFuncs and its first element exist before setting state
        if (valueFuncs.length > 0 && valueFuncs[0]) {
            setInputValues(valueFuncs[0]);
        }
    }, [valueFuncs]);

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
                    table_name={table_name}
                    headers={headers}
                    inputValues={inputValues}
                    handleInputChange={handleInputChange}
                    canEdit={canEdit}
                    submitButtonFunc={submitEditButton}
                    valueFuncs={valueFuncs}
                />
            </div>
        </>
    );
}

// 4. Make InfoCardDatas dynamic by mapping over the values
function InfoCardDatas({ table_name, headers, inputValues, handleInputChange, canEdit, submitButtonFunc, valueFuncs }) {
    const [avatarFile, setAvatarFile] = useState(null);
    const [avatarURL, setAvatarURL] = useState(null);

    return (
        <>
            <div className='info-card-datas'>
                {table_name === 'student' && (
                    <AvatarPicker avatarUpdate={[avatarFile, setAvatarFile, avatarURL, setAvatarURL]} viewOnly={!canEdit} valueFuncs={valueFuncs} loading={true} />
                )}
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

            {canEdit && <button onClick={() => { 
                updateFile('profile-pictures', valueFuncs[0][0].replace(/-/g, ""), inputValues[0].replace(/-/g, ""), avatarFile);
                submitButtonFunc(); 
            }} className='submit-button'>Done</button>}
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
                {(text === "Sex: ") ? (
                    <select value={inputValue || ''} onChange={(e) => { setInputFuncs(e.target.value) }} disabled={!canEdit}>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                ) : (
                    <input value={inputValue || ''} onChange={(e) => { setInputFuncs(e.target.value) }} readOnly={!canEdit} />
                )}
            </div>
        </>
    );
}