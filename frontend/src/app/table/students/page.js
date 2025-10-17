"use client";
import { useEffect, useState } from 'react';
import Table from '../page';
import InsertForm from '../InsertForm';

export default function Students() {
    // State for the insert form fields
    const [id_num, set_id_num] = useState('');
    const [fname, set_fname] = useState('');
    const [lname, set_lname] = useState('');
    const [program_code, set_program_code] = useState('');
    const [year, set_year] = useState('');
    const [sex, set_sex] = useState('');

    // State for table management
    const [table_data, set_table_data] = useState([]);
    const [displayRefresh, setDisplayRefresh] = useState(true);
    const [page, setPage] = useState(1);
    const [maxPage, setMaxPage] = useState(1);
    const [ascending, setAscending] = useState(1);
    const [searchValue, setSearchValue] = useState('');
    const [searchBy, setSearchBy] = useState('id_num'); // Default search attribute
    const [networkError, setNetworkError] = useState(null);

    // Headers for the table and search dropdown
    const headers = ["ID_Num", "Fname", "Lname", "Program", "Year", "Sex"];

    const updateTableData = async () => {
        setDisplayRefresh(true);
        setNetworkError(null);
        try {
            let link = `http://192.168.1.50:5000/get/students/${searchBy}/${page}/${ascending}`;
            if (searchValue.trim() !== '') {
                link = `http://192.168.1.50:5000/search/students/${searchBy}/${searchValue}/${page}/${ascending}`;
            }
            
            const response = await fetch(link);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            set_table_data(data[0]);
            setMaxPage(data[1]);
        } catch (error) {
            console.error("Fetch error:", error);
            setNetworkError("Failed to fetch data from the server. Please check your connection and if the server is running.");
        } finally {
            setDisplayRefresh(false);
        }
    };

    const submitForm = async () => {
        // Frontend validation
        if (!id_num.trim() || !fname.trim() || !lname.trim() || !program_code.trim() || !year.trim() || !sex.trim()) {
            window.alert("All fields must be filled out to add a student.");
            return;
        }
        setNetworkError(null);
        try {
            const response = await fetch(`http://192.168.1.50:5000/insert/student/${id_num}/${fname}/${lname}/${program_code}/${year}/${sex}`);
            if (response.ok) {
                await new Promise(resolve => setTimeout(resolve, 100)); // Small delay for DB to update
                updateTableData();
                clearFields();
            } else {
                const errorData = await response.json();
                setNetworkError(errorData.error || `An unknown error occurred. STATUS: ${response.status}`);
            }
        } catch (error) {
            console.error("Submit error:", error);
            setNetworkError("Failed to submit data. The server might be down.");
        }
    };

    const clearFields = () => {
        set_id_num('');
        set_fname('');
        set_lname('');
        set_program_code('');
        set_year('');
        set_sex('');
    };

    // Effect to fetch data when page, search, or sort criteria change
    useEffect(() => {
        updateTableData();
    }, [page, searchBy, ascending, searchValue]);

    // Effect to handle invalid page numbers
    useEffect(() => {
        if (page > maxPage && maxPage > 0) {
            setPage(maxPage);
        } else if (page <= 0) {
            setPage(1);
        }
    }, [page, maxPage]);

    return (
        <>
            {networkError && <div style={{ color: 'red', textAlign: 'center', padding: '10px', border: '1px solid red', margin: '10px' }}>{networkError}</div>}
            
            <InsertForm 
                fields={[
                    ["ID Number: ", id_num, set_id_num], 
                    ["First Name: ", fname, set_fname], 
                    ["Last Name: ", lname, set_lname], 
                    ["Program Code: ", program_code, set_program_code], 
                    ["Year: ", year, set_year], 
                    ["Sex: ", sex, set_sex]
                ]} 
                submitFunc={submitForm} 
            />
            
            <Table 
                table_name={"student"} 
                headers={headers} 
                table_data={table_data} 
                refreshFunc={updateTableData} 
                displayRefresh={displayRefresh} 
                paginationFunctions={[page, setPage, maxPage]} 
                searchFuncs={[ascending, setAscending, searchValue, setSearchValue, searchBy, setSearchBy]} 
            />
        </>
    )
}