"use client";
import { useEffect, useState } from 'react';
import Table from '../page'
import './colleges.css'
import InsertCollegeForm from './InsertCollegeForm';


export default function Colleges() {
    const [table_data, set_table_data] = useState([]);

    const fetchTableData = async () => {
        const data = await fetch('http://192.168.1.50:5000/get/colleges');
        const result = await data.json();
        set_table_data(result);
        console.log(`Fetching Data: ${result}`);
    };

    useEffect(() => {
        fetchTableData();
    }, [])

    return (
        <>
            <InsertCollegeForm fetchFunc={fetchTableData} />
            
            <Table table_name={"College Table"} headers={["Code", "Name"]} table_data={table_data} />
        </>
    )
}