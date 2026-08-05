"use client";
import './StudentFilter.css'
import { useEffect, useState } from 'react';

const YEAR_OPTIONS = ['1', '2', '3', '4'];

export default function StudentFilter({ StudentFilters=[], visibility=[] }) {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    const filters = StudentFilters[0] || {};
    const setFilters = StudentFilters[1];

    const [programOptions, setProgramOptions] = useState([]);

    // Program codes aren't paginated here since the dropdown needs the full list
    useEffect(() => {
        if (!visibility[0]) return;

        const fetchProgramCodes = async () => {
            try {
                const response = await fetch(`${API_URL}/programs/codes`);
                if (!response.ok) return;
                const data = await response.json();
                setProgramOptions(data);
            } catch (error) {
                console.error("Failed to fetch program codes:", error);
            }
        };
        fetchProgramCodes();
    }, [visibility[0]]);

    const updateFilter = (key, value) => {
        const newFilters = { ...filters };
        if (value) {
            newFilters[key] = value;
        } else {
            delete newFilters[key];
        }
        setFilters(newFilters);
    };

    return (
        <>
            {visibility[0] && (
                <>
                    <div className='out-sf' onClick={() => { visibility[1](false) }} />
                    <div className="card-div-sf">
                        <div className='filter-header-sf'>
                            <label>Filter Students</label>
                        </div>
                        <div style={{width: '100%', border: '1px dashed #2b2b2b'}} />
                        <div className='filter-body-sf'>
                            <div className='filter-row-sf'>
                                <label>Sex</label>
                                <select className='select-sf' value={filters.Sex || ''} onChange={(e) => updateFilter('Sex', e.target.value)}>
                                    <option value=''>All</option>
                                    <option value='Male'>Male</option>
                                    <option value='Female'>Female</option>
                                </select>
                            </div>

                            <div className='filter-row-sf'>
                                <label>Year Level</label>
                                <select className='select-sf' value={filters.Year || ''} onChange={(e) => updateFilter('Year', e.target.value)}>
                                    <option value=''>All</option>
                                    {YEAR_OPTIONS.map((year) => (
                                        <option key={year} value={year}>{year}</option>
                                    ))}
                                </select>
                            </div>

                            <div className='filter-row-sf'>
                                <label>Program</label>
                                <select className='select-sf' value={filters.Program || ''} onChange={(e) => updateFilter('Program', e.target.value)}>
                                    <option value=''>All</option>
                                    {programOptions.map((code) => (
                                        <option key={code} value={code}>{code}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </>
    )
}