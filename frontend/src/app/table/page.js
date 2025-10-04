"use client";
import { useState } from 'react';
import './table.css'
import InsertForm from './InsertForm';
import InfoCard from './InfoCard';

export default function Table({ table_name="Table", headers=["header1", "header2", "header3"], table_data=[] }) {

    const [visibleInfoCard, setVisibleInfoCard] = useState(false);
    const [collegeValue, setCollegeValue] = useState([]);

    return (
    <>
        <InfoCard visibility={[visibleInfoCard, setVisibleInfoCard]} values={collegeValue} />

        <div className='table-header'>
            <label>{table_name}</label>
        </div>

        <div className='my-table'>
            <table> 
                <thead>
                    <tr>
                        {/* <th>First Name</th>
                        <th>Last Name</th>
                        <th>Sex</th>
                        <th>ID Number</th>
                        <th>Year Level</th>
                        <th>College</th>
                        <th>Program</th> */}

                        {headers.map((header) => (
                            <th key={header}>{header}</th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    
                    {table_data.map((coll) => (
                        <tr key={coll[0]} className='h-10 college' onClick={() => {setVisibleInfoCard(true); setCollegeValue([coll[0], coll[1]]);}}>
                            <td>{coll[0]}</td>
                            <td>{coll[1]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </>
    )
}