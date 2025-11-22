"use client";
import { useEffect, useState } from 'react';
import Table from '../page'
import InsertForm from '../InsertForm'


export default function Programs() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const attributes = ["Code", "Name", "College"];
    const [tableName, setTableName] = useState('program');
    const [program_code, set_program_code] = useState('');
    const [program_name, set_program_name] = useState('');
    const [program_college, set_program_college] = useState('');

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
        let link = `${API_URL}/search/programs/${searchBy}/${searchValue}/${page}/${ascending}`;
        if (searchValue === '') {
            link = `${API_URL}/get/programs/${searchBy}/${page}/${ascending}`;
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
        if (!program_code.trim() || !program_name.trim() || !program_college.trim()) {
            window.alert("Please fill out all the fields");
            return; // Stop the function from proceeding
        }
        console.log(`Submitting College [${program_code} | ${program_name} | ${program_college}]`);
        const response = await fetch(`${API_URL}/insert/program/${program_code}/${program_name}/${program_college}`);
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
        set_program_code('');
        set_program_name('');
        set_program_college('');
    };

    return (
        <>
            <InsertForm insert_form_name='Add Program' fields={[
                ["Code: ", program_code, set_program_code], 
                ["Name: ", program_name, set_program_name],
                ["College: ", program_college, set_program_college]
            ]} submitFunc={submitForm} />
            
            <Table table_name={tableName} header_name={'Program Table'} headers={attributes} table_data={table_data} refreshFunc={updateTableData} displayRefresh={displayRefresh} paginationFunctions={[page, setPage, maxPage]} searchFuncs={[ascending, setAscending, searchValue, setSearchValue, searchBy, setSearchBy]} />
        </>
    )
}