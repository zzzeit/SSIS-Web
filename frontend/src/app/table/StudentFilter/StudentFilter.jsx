import './StudentFilter.css'
import { useState } from 'react';

export default function StudentFilter({ StudentFilters=[], visibility=[] }) {
    const [selectValue, setSelectValue] = useState('Program');
    const [inputValue, setInputValue] = useState('');

    return (
        <>
            {visibility[0] && (
                <>
                    <div className='out-sf' onClick={() => {visibility[1](false)}} />
                    <div className="card-div-sf">
                        <div className='add-filter-header-sf'>
                            <select className='select-sf' onChange={(e) => setSelectValue(e.target.value)}>
                                <option value="Program">Program</option>
                                <option value="Year">Year</option>
                                <option value="Sex">Sex</option>
                            </select>
                            <input className='input-sf' placeholder='Value' onChange={(e) => setInputValue(e.target.value)} />
                            <button className='add-filter-sf'     onClick={() => {
                                                                        const newFilters = { ...StudentFilters[0], [selectValue]: inputValue };
                                                                        StudentFilters[1](newFilters);
                                                                        console.log(StudentFilters[0]);
                                                                    }}>
                                <img src='https://cdn-icons-png.flaticon.com/128/992/992651.png' alt='add filter' style={{width: '25px', height: '25px'}} />
                            </button>
                        </div>
                        <div style={{width: '100%', border: '1px dashed #2b2b2b'}} />
                        <div className='filter-body-sf'>
                            {Object.keys(StudentFilters[0]).length === 0 && (
                                <label className='no-filters-sf'>No active filters</label>
                            )}
                            {Object.entries(StudentFilters[0]).map(([key, value]) => (
                                <FilterItem
                                    key={key}
                                    filterKey={key}
                                    filterValue={value}
                                    removeFunc={() => {
                                        const newFilters = { ...StudentFilters[0] };
                                        delete newFilters[key];
                                        StudentFilters[1](newFilters);
                                    }}
                                />
                            ))}
                        </div>
                    </div>
                </>
                
            )}
            
        </>
    )

}

function FilterItem({ filterKey, filterValue, removeFunc }) {
    return (
        <div className='filter-item-sf'>
            <label>{filterKey}: {filterValue}</label>
            <button className='remove-filter-sf' onClick={removeFunc}>
                <img src='https://cdn-icons-png.flaticon.com/128/1828/1828665.png' alt='remove filter' style={{width: '20px', height: '20px'}} />
            </button>
        </div>
    )
}