import './table.css'

export default function Table() {
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
                    <tr>
                        <td>Neil Anthony</td>
                        <td>Balbutin</td>
                        <td>Male</td>
                        <td>2023-0783</td>
                        <td>3rd Year</td>
                        <td>CCS</td>
                        <td>BSCS</td>
                    </tr>
                    <tr>
                        <td>test</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </>
    )
}