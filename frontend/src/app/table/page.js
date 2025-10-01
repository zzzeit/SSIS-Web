import './table.css'

export default async function Table({ table_name="Table", headers=["header1", "header2", "header3"] }) {
    // const data = await fetch('http://127.0.0.1:5000/get/students')
    // const res = await data.json()


    return (
    <>
        <div className='table-header'>
            <label>{table_name}</label>
        </div>
        <div className='my-table'>
            <table> 
                <thead>
                    <tr>
                        {/* <th>First Name</th>
                        <th>Last Name</th>
                        <th>Sex</th>
                        <th>ID Number</th>
                        <th>Year Level</th>
                        <th>College</th>
                        <th>Program</th> */}

                        {headers.map((header) => (
                            <th key={header}>{header}</th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {/* {res.map((student) => (
                        <tr key={student[3]} className='h-10'>
                            <td>{student[0]}</td>
                            <td>{student[1]}</td>
                            <td>{student[2]}</td>
                            <td>{student[3]}</td>
                            <td>{student[4]}</td>
                            <td>{student[5]}</td>
                            <td>{student[6]}</td>
                        </tr>
                    ))} */}
                </tbody>
            </table>
        </div>
    </>
    )
}