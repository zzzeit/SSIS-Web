"use client";
import { useEffect, useState } from 'react';
import Table from '../page'
import InsertForm from '../InsertForm'


export default function Colleges() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

    const [tableName, setTableName] = useState('college');
    const [college_code, set_college_code] = useState('');
    const [college_name, set_college_name] = useState('');

    const [table_data, set_table_data] = useState([]);
    const [displayRefresh, setDisplayRefresh] = useState(false);
    const [page, setPage] = useState(1);
    const [maxPage, setMaxPage] = useState(1);
    const [ascending, setAscending] = useState(1);
    const [searchValue, setSearchValue] = useState('');
    const [searchBy, setSearchBy] = useState('code');

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
    }, [ascending, searchBy]);

    const clearFields = () => {
        set_college_code('');
        set_college_name('');
    };

    const updateTableData = async () => {
        setDisplayRefresh(true);
        console.log(`Fetching Data...`);
        let link = `${API_URL}/colleges?attribute=${searchBy}&page=${page}&ascending=${ascending}&value=${searchValue}`;
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
        const response = await fetch(`${API_URL}/colleges`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "code": college_code, "name": college_name })
        });
        if (response.status === 201) {
            await new Promise(resolve => setTimeout(resolve, 100));
            updateTableData();
            clearFields();
        } else {
            const errorData = await response.json();
            window.alert(errorData.error || `An unknown error has occured. STATUS ${response.status}`);
        }
    };

    const submitEditButton = async (valueFuncs, inputValues, refreshFunc, visibilityFunc) => {
        const oldCode = valueFuncs[0]?.[0];
        if (!oldCode) return;

        // 1. Use the whole inputValues array, not just the first two items.
        const newValues = inputValues;

        // 2. Basic validation to ensure no fields are empty.
        if (newValues.some(val => !val || String(val).trim() === '')) {
            window.alert("All fields must be filled out before submitting.");
            return;
        }

        // 3. Dynamically create the URL path from all the new values.
        const newValuesPath = newValues.join('/');

        // 4. Make the confirmation message more generic.
        const isConfirm = window.confirm(`Are you sure you want to save these changes for item ${oldCode}?`);
        if (isConfirm) {
            // 5. Construct the final URL dynamically.
            const url = `${API_URL}/colleges/edit/${oldCode}`;
            console.log("Submitting edit request to:", url);

            const response = await fetch(url, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "code": newValues[0], "name": newValues[1] })
            });
            if (response.ok) {
                refreshFunc();
                visibilityFunc();
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occurred. STATUS ${response.status}`);
            }
        }
    };

    const deleteFunc = async (valueFuncs, refreshFunc, visibilityFunc) => {
        const oldCode = valueFuncs[0]?.[0];
        if (!oldCode) return;

        const isConfirm = window.confirm(`Are you sure you want to delete ${oldCode}?`);
        if (isConfirm) {
            const response = await fetch(`${API_URL}/colleges/delete/${oldCode}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                refreshFunc();
                visibilityFunc();
            } else {
                const errorData = await response.json();
                window.alert(errorData.error || `An unknown error has occurred. STATUS ${response.status}`);
            }
        }
    }

    return (
        <>
            <InsertForm fields={[["Code: ", college_code, set_college_code], ["Name: ", college_name, set_college_name]]} submitFunc={submitForm} />
            
            <Table 
                table_name={tableName} 
                header_name={"College Table"} 
                headers={["Code", "Name"]} 
                table_data={table_data} 
                refreshFunc={updateTableData} 
                displayRefresh={displayRefresh} 
                paginationFunctions={[page, setPage, maxPage]} 
                searchFuncs={[ascending, setAscending, searchValue, setSearchValue, searchBy, setSearchBy]} 
                editDeleteFuncs={[ submitEditButton, deleteFunc ]}
                 />
        </>
    )
}