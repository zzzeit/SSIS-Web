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
    const [ascending, setAscending] = useState(1);
    const [searchValue, setSearchValue] = useState('');
    const [searchBy, setSearchBy] = useState('code');

    const updateTableData = async () => {
        setDisplayRefresh(true);
        console.log(`Fetching Data...`);
        let link = `http://192.168.1.50:5000/search/colleges/${searchBy}/${searchValue}/${page}/${ascending}`;
        if (searchValue === '') {
            link = `http://192.168.1.50:5000/get/colleges/${searchBy}/${page}/${ascending}`;
        }
        const response = await fetch(link);
        if (response.status === 200) {
            const data = await response.json();
            set_table_data(data[0]);
            setMaxPage(data[1]);
        } else {
            const errorData = await response.json();
            window.alert(errorData.error || `An unknown error has occured. STATUS ${response.status}`);
        }
        setDisplayRefresh(false);
    };


    const submitForm = async () => {
        if (!college_code.trim() || !college_name.trim()) {
            window.alert("College Code and Name cannot be empty.");
            return; // Stop the function from proceeding
        }
        console.log(`Submitting College [${college_code} | ${college_name}]`);
        const response = await fetch(`http://192.168.1.50:5000/insert/college/${college_code}/${college_name}`);
        if (response.status === 201) {
            await new Promise(resolve => setTimeout(resolve, 100));
            updateTableData();
            clearFields();
        } else {
            const errorData = await response.json();
            window.alert(errorData.error || `An unknown error has occured. STATUS ${response.status}`);
        }
    };

    useEffect(() => {
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

    useEffect(() => {
        setPage(1);
        updateTableData();

    }, [searchValue]);

    useEffect(() => {
        updateTableData();
        
    }, [ascending]);

    useEffect(() => {
        updateTableData();
    }, [searchBy]);

    const clearFields = () => {
        set_college_code('');
        set_college_name('');
    };

    return (
        <>
            <InsertForm fields={[["Code: ", college_code, set_college_code], ["Name: ", college_name, set_college_name]]} submitFunc={submitForm} />
            
            <Table table_name={"College Table"} headers={["Code", "Name"]} table_data={table_data} refreshFunc={updateTableData} displayRefresh={displayRefresh} paginationFunctions={[page, setPage, maxPage]} searchFuncs={[ascending, setAscending, searchValue, setSearchValue, searchBy, setSearchBy]} />
        </>
    )
}