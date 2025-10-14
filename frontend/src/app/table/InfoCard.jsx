"use client";
import './InfoCard.css'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import { useEffect, useState } from 'react';

export default function InfoCard({visibility, valueFuncs=[], refreshFunc}) {
    const [canEdit, setCanEdit] = useState(false);

    const [codeInput, setCodeInput] = useState('');
    const [nameInput, setNameInput] = useState('');

    const deleteFunc = async () => {
        const isConfirm = window.confirm(`Are you sure you want to delete ${valueFuncs[0][0]}?`);
        if (isConfirm) {
            const response = await fetch(`http://192.168.1.50:5000/delete/college/${valueFuncs[0][0]}`);
            if (response.status === 200) {
                refreshFunc();
                visibilityFunc();
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occured. STATUS ${response.status}`);
            }

        }
    }

    const visibilityFunc = () => {
        visibility[1](false);
        setCanEdit(false);

        setCodeInput('');
        setNameInput('');
    };

    const submitEditButton = async () => {
        console.log(`Changing college ${valueFuncs[0][0]} into ${codeInput} - ${nameInput}`)
        const isConfirm = window.confirm(`Are you sure you want to edit ${valueFuncs[0][0]} into ${codeInput} - ${nameInput}?`);
        if (isConfirm) {
            const response = await fetch(`http://192.168.1.50:5000/edit/college/${valueFuncs[0][0]}/${codeInput}/${nameInput}`);
            if (response.status === 200) {
                refreshFunc();
                visibilityFunc();       
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occured. STATUS ${response.status}`);
            }
        }

    };

    useEffect(() => {
        setCodeInput(valueFuncs[0][0]);
        setNameInput(valueFuncs[0][1]);
    }, [valueFuncs[0]]);

    if (!visibility[0] || valueFuncs.length === 0) {
        return null;
    }

    return (
        <>
            <div className="bg-pop-up" onClick={() => {visibilityFunc()}} />

            <div className="pop-up">
                <div className='header-pop-up'>
                    <HeaderButton onClick={() => {visibilityFunc()}} style={{borderTopRightRadius: '10px', width: '45px'}}>
                        <Image src='/close.svg' alt='Close' width={28} height={28} style={{filter: 'var(--svg-inverse)'}} />
                    </HeaderButton>
                    <HeaderButton onClick={() => {deleteFunc();}} style={{width: '45px'}}>
                        <Image src={'/trash.svg'} alt='Trash' width={28} height={28} style={{filter: 'var(--svg-inverse)'}} />
                    </HeaderButton>
                    <HeaderButton onClick={() => {
                        setCodeInput(valueFuncs[0][0]);
                        setNameInput(valueFuncs[0][1]);
                        setCanEdit(!canEdit);
                    }} style={{width: '45px'}}>
                        <Image src={'/edit.svg'} alt='Edit' width={28} height={28} style={{filter: 'var(--svg-inverse)'}} />
                    </HeaderButton>

                </div>

                <InfoCardDatas valueFuncs={valueFuncs} inputFuncs={[codeInput, setCodeInput, nameInput, setNameInput]} canEdit={canEdit} submitButtonFunc={submitEditButton} />
                
            </div>
        </>
    );
}

function InfoCardDatas({valueFuncs=[], inputFuncs=[], canEdit, submitButtonFunc}) {
    
    return (
        <>
            <div className='info-card-datas'>
                <InfoCardData text='Code: ' inputValue={inputFuncs[0]} setInputFuncs={inputFuncs[1]} canEdit={canEdit} />
                <InfoCardData text='Name: ' inputValue={inputFuncs[2]} setInputFuncs={inputFuncs[3]} canEdit={canEdit} />
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
                <input value={inputValue} onChange={(e) => {setInputFuncs(e.target.value)}} readOnly={!canEdit} />
            </div>
        </>
    );

}