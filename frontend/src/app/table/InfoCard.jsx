"use client";
import './InfoCard.css'
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import { useState } from 'react';

export default function InfoCard({visibility, values, setValue, refreshFunc}) {
    const [canEdit, setCanEdit] = useState(false);

    const [codeInput, setCodeInput] = useState('');
    const [nameInput, setNameInput] = useState('');

    const deleteFunc = async () => {
        const isConfirm = window.confirm(`Are you sure you want to delete ${values[0]}?`);

        if (isConfirm) {
            const d = await fetch(`http://192.168.1.50:5000/delete/college/${values[0]}`);
            console.log(d);
        }
        refreshFunc();
    }

    const visibilityFunc = () => {
        visibility[1](false);
        setCanEdit(false);
    };

    const submitEditButton = async () => {
        console.log(`Changing college ${values[0]} into ${codeInput} - ${nameInput}`)
        await fetch(`http://192.168.1.50:5000/edit/college/${values[0]}/${codeInput}/${nameInput}`);
        refreshFunc();
        visibilityFunc();
    };

    if (!visibility[0]) {
        return null;
    }

    return (
        <>
            <div className="bg-pop-up" onClick={() => {visibilityFunc()}} />

            <div className="pop-up">
                <div className='header-pop-up'>
                    <HeaderButton onClick={() => {visibilityFunc()}} style={{borderTopRightRadius: '10px', width: '45px'}}>
                        <Image src='/close.svg' alt='Close' width={28} height={28} className='invert' />
                    </HeaderButton>
                    <HeaderButton onClick={() => {deleteFunc();}} style={{width: '45px'}}>
                        <Image src={'/trash.svg'} alt='Trash' width={28} height={28} className='invert' />
                    </HeaderButton>
                    <HeaderButton onClick={() => {setCodeInput(values[0]);setNameInput(values[1]);setCanEdit(!canEdit);}} style={{width: '45px'}}>
                        <Image src={'/edit.svg'} alt='Edit' width={28} height={28} className='invert' />
                    </HeaderButton>

                </div>

                <InfoCardDatas values={values} setFuncs={[setCodeInput, setNameInput]} canEdit={canEdit} submitButtonFunc={submitEditButton} />
                
            </div>
        </>
    );
}

function InfoCardDatas({values, setFuncs, canEdit, submitButtonFunc}) {
    
    return (
        <>
            <div className='info-card-datas'>
                <InfoCardData text='Code: ' value={values[0]} setFunc={setFuncs[0]} canEdit={canEdit} />
                <InfoCardData text='Name: ' value={values[1]} setFunc={setFuncs[1]} canEdit={canEdit} />
            </div>

            {canEdit && <button onClick={submitButtonFunc} className='submit-button'>Done</button>}

        </>
    );
}

function InfoCardData({text='Label: ', value='None', setFunc, canEdit}) {
    let classVar = 'info-card-data';
    if (canEdit) {
        classVar = 'info-card-data-editable';
    }
    return (
        <>
            <div className={classVar}>
                <label>{text}</label>
                <input defaultValue={value} onChange={(e) => {setFunc(e.target.value)}} readOnly={!canEdit} />
            </div>
        </>
    );

}