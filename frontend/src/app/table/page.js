"use client";
import { useEffect, useState } from 'react';
import './table.css'
import InfoCard from './InfoCard';
import InsertForm from './InsertForm';
import StudentFilter from './StudentFilter/StudentFilter';
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import Lottie from 'lottie-react';
import loadingIcon from './loading.json';
import Button from '../Button';
import LogoutButton from './LogoutButton';
import { deleteFile, getFileUrl } from '@/utils/supaClient';

const DEFAULT_AVATAR_URL = 'https://cdn-icons-png.flaticon.com/128/9308/9308008.png';

export default function Table({ table_name="Table", header_name="", headers=["header1", "header2", "header3"], table_data=[], refreshFunc, displayRefresh, paginationFunctions=[], searchFuncs=[], editDeleteFuncs=[], StudentFilters=[], insertForm=null }) {

    const [visibleInfoCard, setVisibleInfoCard] = useState(false);
    const [visibleStudentFilter, setVisibleStudentFilter] = useState(false);
    const [selectedRow, setSelectedRow] = useState([]);
    const [editMode, setEditMode] = useState(false);

    useEffect(() => {
        if (visibleStudentFilter === false) {
            refreshFunc();
        }
        
    }, [visibleStudentFilter]);

    // Opens the InfoCard, optionally starting straight in edit mode
    const openInfoCard = (row, startInEdit = false) => {
        setSelectedRow(row);
        setEditMode(startInEdit);
        setVisibleInfoCard(true);
    };

    const deleteRow = async (row) => {
        const oldCode = row?.[0];
        if (!oldCode) return;

        const isConfirm = window.confirm(`Are you sure you want to delete ${oldCode}?`);
        if (!isConfirm) return;

        if (table_name === 'student' && !(await deleteFile('profile-pictures', `${String(oldCode).replace(/-/g, "")}`))) {
            console.error("Failed to delete profile picture.");
        }
        if (typeof editDeleteFuncs[1] === 'function') {
            editDeleteFuncs[1]([row], refreshFunc, () => setVisibleInfoCard(false));
        }
    };

    return (
    <>
        <InfoCard table_name={table_name} headers={headers} visibility={[visibleInfoCard, setVisibleInfoCard]} valueFuncs={[selectedRow, setSelectedRow]} refreshFunc={refreshFunc} editDeleteFuncs={editDeleteFuncs} initialEdit={editMode} />
        <StudentFilter StudentFilters={StudentFilters} visibility={[visibleStudentFilter, setVisibleStudentFilter]} />
        
        
        <div className='table-header'>
            <label>{header_name}</label>
            {/* <HeaderButton className='inline right-auto'>
                <Lottie animationData={serverIcon} style={{width: '40px',height: '40px'}} loop autoPlay />
            </HeaderButton> */}
        </div>

        <SearchBarComponent headers={headers} funcs={searchFuncs} StudentFilterVisibility={[visibleStudentFilter, setVisibleStudentFilter]} insertForm={insertForm} />

        <TableComponent
            table_name={table_name}
            headers={headers}
            table_data={table_data}
            displayRefresh={displayRefresh}
            paginationFunctions={paginationFunctions}
            searchFuncs={searchFuncs}
            onView={(row) => openInfoCard(row, false)}
            onEdit={(row) => openInfoCard(row, true)}
            onDelete={deleteRow}
        />

        <Pagination paginationFunctions={paginationFunctions} />

        <LogoutButton />
    </>
    )
}

function SearchBarComponent({headers=[], funcs=[], StudentFilterVisibility=[], insertForm=null}) {

    return (
        <>
            <div className='search-div'>
                <select onChange={(e) => {funcs[5](e.target.value)}}>
                    {headers.map((att) => (
                        <option key={att} value={att}>{att}</option>
                    ))}
                </select>

                <input placeholder='Search' onChange={(e) => {
                    funcs[3](e.target.value)
                }} />
                {headers[0]==="ID_Num" && (
                    <Button className='search-button' >
                        <img src='https://cdn-icons-png.flaticon.com/128/2676/2676824.png' alt='filter icon' style={{width: 25, height: 25, filter: 'invert(1)', transform: 'rotate(180deg)'}} onClick={() => {
                        StudentFilterVisibility[1](true);
                        console.log('Filter button clicked');
                    }} />
                    </Button>    
                )}

                {insertForm && (
                    <InsertForm
                        insert_form_name={insertForm.name}
                        fields={insertForm.fields}
                        submitFunc={insertForm.submitFunc}
                        avatarUpdate={insertForm.avatarUpdate}
                    />
                )}
                
            </div>
        </>
    );
}

function TableComponent({table_name, headers, table_data, displayRefresh, paginationFunctions=[], searchFuncs=[], onView, onEdit, onDelete}) {

    const [ascending, setAscending, , , searchBy, setSearchBy] = searchFuncs;
    const showPfp = table_name === 'student';

    const sortByHeader = (header) => {
        if (typeof setSearchBy !== 'function' || typeof setAscending !== 'function') return;
        if (searchBy && String(searchBy).toLowerCase() === header.toLowerCase()) {
            setAscending(ascending === 1 ? 0 : 1);
        } else {
            setSearchBy(header);
            setAscending(1);
        }
    };

    return (
        <>
            <div className='my-table'>
                
                <RefreshDisplay display={displayRefresh} />
                <table> 
                    <thead>
                        <tr>
                            <th style={{width: '50px'}}>#</th>
                            {showPfp && <th style={{width: '50px'}}>Pfp</th>}
                            {headers.map((header) => {
                                const isActive = searchBy && String(searchBy).toLowerCase() === header.toLowerCase();
                                return (
                                    <th key={header} className='sortable-header' onClick={() => sortByHeader(header)}>
                                        {header}
                                        <span className='sort-indicator'>{isActive ? (ascending === 1 ? '↑' : '↓') : ''}</span>
                                    </th>
                                );
                            })}
                            <th style={{width: '90px'}}>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        
                        {table_data.map((row, index) => (
                            <tr key={row[0] || index} className='h-10 college' onClick={() => onView(row)}>
                                
                                <td>{(index + 1) + ((paginationFunctions[0] - 1) * 14)}</td>

                                {showPfp && (
                                    <td onClick={(e) => e.stopPropagation()}>
                                        <StudentAvatarCell id_num={row[0]} />
                                    </td>
                                )}

                                {row.map((cell, cellIndex) => (
                                    <td key={cellIndex}>{cell}</td>
                                ))}

                                <td className='action-cell' onClick={(e) => e.stopPropagation()}>
                                    <button type='button' className='action-button-edit' onClick={() => onEdit(row)}>
                                        <Image src='/media/edit.svg' alt='Edit' width={18} height={18} style={{ filter: 'var(--svg-inverse)' }} />
                                    </button>
                                    <button type='button' className='action-button-delete' onClick={() => onDelete(row)}>
                                        <Image src='/media/trash.svg' alt='Delete' width={18} height={18} style={{ filter: 'var(--svg-inverse)' }} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    );
}

function StudentAvatarCell({id_num}) {
    // Stays null (unresolved) until the lookup confirms whether a pfp exists
    const [avatarURL, setAvatarURL] = useState(null);

    useEffect(() => {
        let isMounted = true;
        setAvatarURL(null);

        const fetchAvatar = async () => {
            if (!id_num) {
                if (isMounted) setAvatarURL(DEFAULT_AVATAR_URL);
                return;
            }
            const url = await getFileUrl('profile-pictures', String(id_num).replace(/-/g, ""));
            if (isMounted) {
                setAvatarURL(url || DEFAULT_AVATAR_URL);
            }
        };
        fetchAvatar();

        return () => { isMounted = false; };
    }, [id_num]);

    if (!avatarURL) {
        return <div className='table-avatar table-avatar-placeholder' />;
    }

    return (
        <img
            src={avatarURL}
            alt='pfp'
            className='table-avatar'
            onError={(e) => { e.currentTarget.src = DEFAULT_AVATAR_URL; }}
        />
    );
}

function RefreshDisplay({display}) {
    if (display) {
        return (
            <>
            <div className='refresh-display'>
                <Lottie animationData={loadingIcon} style={{width: 250, height: 250, filter: 'invert(1)'}} loop autoPlay speed={0.5} />
            </div>
            </>
        );
    }
}

function Pagination({paginationFunctions=[]}) {

    return (
        <>
            <div className='footer'>

                <div className='pagination'>
                    <HeaderButton style={{width: '45px', borderTopLeftRadius: '10px', borderBottomLeftRadius: '10px'}} onClick={() => {
                            if (
                                paginationFunctions[0] !== undefined &&
                                paginationFunctions[0] !== null &&
                                !isNaN(parseInt(paginationFunctions[0]))
                            ) {
                                paginationFunctions[1](parseInt(paginationFunctions[0]) - 1);                   
                            }                        
                        }} >
                        <Image src={"/media/arrow-left.svg"} alt='previous page' width={24} height={24} style={{filter: 'var(--svg-inverse)'}} />
                    </HeaderButton>

                    <div className='pagination-input'>
                        <input className='w-7 text-center' value={paginationFunctions[0]} onChange={(e) => {paginationFunctions[1](e.target.value)}} />
                        <label>{` of ${paginationFunctions[2]}`}</label>
                    </div>

                    <HeaderButton style={{width: '45px', borderTopRightRadius: '10px', borderBottomRightRadius: '10px'}} onClick={() => {
                            if (
                                paginationFunctions[0] !== undefined &&
                                paginationFunctions[0] !== null &&
                                !isNaN(parseInt(paginationFunctions[0]))
                            ) {
                                paginationFunctions[1](parseInt(paginationFunctions[0]) + 1);                   
                            }
                        }}>
                        <Image src={"/media/arrow-left.svg"} alt='next page' width={24} height={24} style={{filter: 'var(--svg-inverse)', transform: 'rotate(180deg)'}} />
                    </HeaderButton>
                </div>

            </div>
        </>
    );
}