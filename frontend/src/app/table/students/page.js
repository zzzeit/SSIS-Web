"use client";
import { useEffect, useState } from 'react';
import { uploadFile } from '@/utils/supaClient';
import Table from '../page';
import InsertForm from '../InsertForm';

export default function Students() {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;

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

    // State for avatar
    const [avatarFile, setAvatarFile] = useState(null);
    const [avatarURL, setAvatarURL] = useState(null);

    // Headers for the table and search dropdown
    const headers = ["ID_Num", "Fname", "Lname", "Program", "Year", "Sex"];

    // Filters
    const [StudentFilters, setStudentFilters] = useState({});

    const clearFields = () => {
        set_id_num('');
        set_fname('');
        set_lname('');
        set_program_code('');
        set_year('');
        set_sex('');
        setAvatarFile(null);
        setAvatarURL(null);
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

    const updateTableData = async () => {
        setDisplayRefresh(true);
        setNetworkError(null);
        try {
            let link = `${API_URL}/students?attribute=${searchBy}&page=${page}&ascending=${ascending}&value=${searchValue}`;
            
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

    const uploadAvatar = async () => {
        if (!id_num || !avatarFile) return;
        const remotePath = `${id_num.replace(/-/g, "")}`;
        const response = await uploadFile('profile-pictures', remotePath, avatarFile);
        if (!response) {
            return false;
        }
        return true;
    }

    const submitForm = async () => {
        setNetworkError(null);
        try {
            if (!avatarFile) {
                window.alert("Student needs a profile picture.");
                return;
            } else if (!(await uploadAvatar())) {
                window.alert("Failed to upload avatar. Insert student failed.");
                return;
            }
            const response = await fetch(`${API_URL}/students`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "id_num": id_num, "fname": fname, "lname": lname, "program_code": program_code, "year": year, "sex": sex })
            });
            if (response.ok) {
                await new Promise(resolve => setTimeout(resolve, 100)); // Small delay for DB to update
                updateTableData();
                clearFields();
            } else {
                const errorData = await response.json();
                console.error("Submit error response:", errorData);
                setNetworkError(errorData.error || `An unknown error occurred. STATUS: ${response.status}`);
            }
        } catch (error) {
            console.error("Submit error:", error);
            setNetworkError("Failed to submit data. The server might be down.");
        }
    };

    const submitEditButton = async (valueFuncs, inputValues, refreshFunc, visibilityFunc) => {
        const oldCode = valueFuncs[0]?.[0];
        if (!oldCode) return;

        const newValues = inputValues;
        if (newValues.some(val => !val || String(val).trim() === '')) {
            window.alert("All fields must be filled out before submitting.");
            return;
        }

        const isConfirm = window.confirm(`Are you sure you want to save these changes for item ${oldCode}?`);
        if (isConfirm) {
            const url = `${API_URL}/students/edit/${oldCode}`;
            console.log("Submitting edit request to:", url);

            const response = await fetch(url, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "id_num": newValues[0], "fname": newValues[1], "lname": newValues[2], "program_code": newValues[3], "year": newValues[4], "sex": newValues[5] })
            });
            if (response.ok) {
                refreshFunc();
                visibilityFunc();
                return true;
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
            const response = await fetch(`${API_URL}/students/delete/${oldCode}`, {
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
            {networkError && <div style={{ color: 'red', textAlign: 'center', padding: '10px', border: '1px solid red', margin: '10px' }}>{networkError}</div>}
            
            <InsertForm 
            insert_form_name='Insert Student'
                fields={[
                    ["ID Number: ", id_num, set_id_num], 
                    ["First Name: ", fname, set_fname], 
                    ["Last Name: ", lname, set_lname], 
                    ["Program Code: ", program_code, set_program_code], 
                    ["Year: ", year, set_year], 
                    ["Sex: ", sex, set_sex]
                ]} 
                submitFunc={submitForm} 
                avatarUpdate={[avatarFile, setAvatarFile, avatarURL, setAvatarURL]}
            />
            
            <Table 
                table_name={"student"} 
                headers={headers} 
                table_data={table_data} 
                refreshFunc={updateTableData} 
                displayRefresh={displayRefresh} 
                paginationFunctions={[page, setPage, maxPage]} 
                searchFuncs={[ascending, setAscending, searchValue, setSearchValue, searchBy, setSearchBy]}
                editDeleteFuncs={[submitEditButton, deleteFunc]} 
                StudentFilters={[StudentFilters, setStudentFilters]}
            />
        </>
    )
}