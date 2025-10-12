"use client";
import { use, useEffect, useState } from 'react';
import Table from '../page'
import InsertForm from '../InsertForm'


export default function Colleges() {
    const [college_code, set_college_code] = useState('');
    const [college_name, set_college_name] = useState('');

    const [table_data, set_table_data] = useState([]);
    const [displayRefresh, setDisplayRefresh] = useState(false);
    const [page, setPage] = useState(1);
    const [maxPage, setMaxPage] = useState(1);

    const updateTableData = async () => {
        setDisplayRefresh(true);
        console.log(`Fetching Data...`);
        const data = await fetch(`http://192.168.1.50:5000/get/colleges/${page}`);
        const result = await data.json();
        set_table_data(result[0]);
        setMaxPage(result[1]);
        setDisplayRefresh(false);
    };

    useEffect(() => {
        setDisplayRefresh(false);
        if (page > maxPage) {
            setPage(maxPage);
        } else if (page === 0) {
            setPage(1);
        } else if (page < 0) {
            setPage(1);
        } else {
            updateTableData();
        }

    }, [page]);

    const submitForm = () => {
        console.log(`Submitting College [${college_code} | ${college_name}]`);
        fetch(`http://192.168.1.50:5000/insert/college/${college_code}/${college_name}`);
    };

    const clearFields = () => {
        set_college_code('');
        set_college_name('');
    };


    return (
        <>
            <InsertForm fields={[["Code: ", college_code, set_college_code], ["Name: ", college_name, set_college_name]]} functions={[updateTableData, submitForm, clearFields]} />
            
            <Table table_name={"College Table"} headers={["Code", "Name"]} table_data={table_data} refreshFunc={updateTableData} displayRefresh={displayRefresh} paginationFunctions={[page, setPage, maxPage]} />
        </>
    )
}