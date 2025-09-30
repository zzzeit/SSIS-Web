import './table.css'

export default async function Table() {
    const data = await fetch('http://127.0.0.1:5000/get/students')
    const res = await data.json()
    const myString = await JSON.stringify(res, null, 2)

    console.log(res)

    return (
    <>
        <div className='my-table'>
            <table> 
                <thead>
                    <tr>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Sex</th>
                        <th>ID Number</th>
                        <th>Year Level</th>
                        <th>College</th>
                        <th>Program</th>
                    </tr>
                </thead>

                <tbody>
                    {res.map((student) => (
                        <tr key={student[3]} className='h-10'>
                            <td>{student[0]}</td>
                            <td>{student[1]}</td>
                            <td>{student[2]}</td>
                            <td>{student[3]}</td>
                            <td>{student[4]}</td>
                            <td>{student[5]}</td>
                            <td>{student[6]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </>
    )
}