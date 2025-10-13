"use client";
import { useState } from 'react';
import './table.css'
import InfoCard from './InfoCard';
import HeaderButton from '../HeaderButton';
import Image from 'next/image';
import Lottie from 'lottie-react';
import loadingIcon from './loading.json';
import Button from '../Button';

export default function Table({ table_name="Table", headers=["header1", "header2", "header3"], table_data=[], refreshFunc, displayRefresh, paginationFunctions=[], searchFuncs=[] }) {

    const [visibleInfoCard, setVisibleInfoCard] = useState(false);
    const [collegeValue, setCollegeValue] = useState([]);

    return (
    <>
        <InfoCard visibility={[visibleInfoCard, setVisibleInfoCard]} values={collegeValue} setValue={setCollegeValue} refreshFunc={refreshFunc} />

        <div className='table-header'>
            <label>{table_name}</label>
            {/* <HeaderButton className='inline right-auto'>
                <Lottie animationData={serverIcon} style={{width: '40px',height: '40px'}} loop autoPlay />
            </HeaderButton> */}
        </div>

        <SearchBarComponent funcs={searchFuncs} />

        <TableComponent headers={headers} table_data={table_data} setFunctions={[setVisibleInfoCard, setCollegeValue]} displayRefresh={displayRefresh} />

        <Pagination paginationFunctions={paginationFunctions} />
    </>
    )
}

function SearchBarComponent({funcs=[]}) {

    return (
        <>
            <div className='search-div'>
                <Button className='search-button' ascending={funcs[0]}>
                    <Image src={'/sort.svg'} alt='sort button' width={25} height={25} style={{ filter: 'invert(1)' }} onClick={() => {
                        funcs[1](funcs[0] === 1 ? 0 : 1)
                    }} />
                </Button>

                <select onChange={(e) => {funcs[5](e.target.value)}}>
                    <option value='code'>Code</option>
                    <option value='name'>Name</option>
                </select>

                <input placeholder='Search' onChange={(e) => {
                    funcs[3](e.target.value)
                }} />
            </div>
        </>
    );
}

function TableComponent({headers, table_data, setFunctions=[], displayRefresh}) {

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
                        
                        {table_data.map((coll, index) => (
                            <tr key={coll[0]} className='h-10 college' onClick={() => {setFunctions[0](true); setFunctions[1]([coll[0], coll[1]]);}}>
                                
                                <td>{index + 1}</td>

                                <td>{coll[0]}</td>
                                <td>{coll[1]}</td>
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
                        <Image src={"/arrow-left.svg"} alt='previous page' width={24} height={24} style={{filter: 'var(--svg-inverse)'}} />
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
                        <Image src={"/arrow-left.svg"} alt='next page' width={24} height={24} style={{filter: 'var(--svg-inverse)', transform: 'rotate(180deg)'}} />
                    </HeaderButton>
                </div>

            </div>
        </>
    );
}