"use client";
import { useEffect, useState } from 'react';
import Table from '../page'
import InsertForm from '../InsertForm'


export default function Colleges() {
    const [college_code, set_college_code] = useState('');
    const [college_name, set_college_name] = useState('');

    const [table_data, set_table_data] = useState([]);

    const updateTableData = async () => {
        const data = await fetch('http://192.168.1.50:5000/get/colleges');
        const result = await data.json();
        set_table_data(result);
        console.log(`Fetching Data: ${result}`);
    };

    const submitForm = () => {
        console.log("Submitting College");
        fetch(`http://192.168.1.50:5000/insert/college/${college_code}/${college_name}`);
    };

    const clearFields = () => {
        set_college_code('');
        set_college_name('');
    };

    useEffect(() => {
        updateTableData();
    }, [])

    return (
        <>
            <InsertForm fields={[["Code: ", college_code, set_college_code], ["Name: ", college_name, set_college_name]]} functions={[updateTableData, submitForm, clearFields]} />
            
            <Table table_name={"College Table"} headers={["Code", "Name"]} table_data={table_data} />
        </>
    )
}