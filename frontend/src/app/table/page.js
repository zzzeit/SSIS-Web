"use client";
import { useState } from 'react';
import './table.css'
import InfoCard from './InfoCard';
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import Lottie from 'lottie-react';
import loadingIcon from './loading.json';
import Button from '../Button';
import LogoutButton from './LogoutButton';

export default function Table({ table_name="Table", header_name="", headers=["header1", "header2", "header3"], table_data=[], refreshFunc, displayRefresh, paginationFunctions=[], searchFuncs=[], editDeleteFuncs=[] }) {

    const [visibleInfoCard, setVisibleInfoCard] = useState(false);
    const [selectedRow, setSelectedRow] = useState([]);

    return (
    <>
        <InfoCard table_name={table_name} headers={headers} visibility={[visibleInfoCard, setVisibleInfoCard]} valueFuncs={[selectedRow, setSelectedRow]} refreshFunc={refreshFunc} editDeleteFuncs={editDeleteFuncs} />

        <div className='table-header'>
            <label>{header_name}</label>
            {/* <HeaderButton className='inline right-auto'>
                <Lottie animationData={serverIcon} style={{width: '40px',height: '40px'}} loop autoPlay />
            </HeaderButton> */}
        </div>

        <SearchBarComponent headers={headers} funcs={searchFuncs} />

        <TableComponent headers={headers} table_data={table_data} setFunctions={[setVisibleInfoCard, setSelectedRow]} displayRefresh={displayRefresh} paginationFunctions={paginationFunctions} />

        <Pagination paginationFunctions={paginationFunctions} />

        <LogoutButton />
    </>
    )
}

function SearchBarComponent({headers=[], funcs=[]}) {

    return (
        <>
            <div className='search-div'>
                <Button className='search-button' ascending={funcs[0]}>
                    <Image src={'/media/sort.svg'} alt='sort button' width={25} height={25} style={{ filter: 'invert(1)' }} onClick={() => {
                        funcs[1](funcs[0] === 1 ? 0 : 1)
                    }} />
                </Button>

                <select onChange={(e) => {funcs[5](e.target.value)}}>
                    {headers.map((att) => (
                        <option key={att} value={att}>{att}</option>
                    ))}
                </select>

                <input placeholder='Search' onChange={(e) => {
                    funcs[3](e.target.value)
                }} />
            </div>
        </>
    );
}

function TableComponent({headers, table_data, setFunctions=[], displayRefresh, paginationFunctions=[]}) {

    return (
        <>
            <div className='my-table'>
                
                <RefreshDisplay display={displayRefresh} />
                <table> 
                    <thead>
                        <tr>
                            <th style={{width: '50px'}}>#</th>
                            {headers.map((header) => (
                                <th key={header}>{header}</th>
                            ))}
                        </tr>
                    </thead>

                    <tbody>
                        
                        {table_data.map((row, index) => (
                            <tr key={row[0] || index} className='h-10 college' onClick={() => {
                                // Pass the entire row array to the InfoCard
                                setFunctions[1](row);
                                setFunctions[0](true); 
                            }}>
                                
                                <td>{(index + 1) + ((paginationFunctions[0] - 1) * 14)}</td>

                                {row.map((cell, cellIndex) => (
                                    <td key={cellIndex}>{cell}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
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