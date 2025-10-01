import Table from '../page'
import './colleges.css'

export default function Colleges() {
    return (
        <>
            <Table table_name={"College Table"} headers={["Code", "Name"]} />
            <div className='insert'>
                <div className='insert-header'>
                    <label>Insert College</label>
                </div>
                <div className='insert-inputs'>
                    <div>
                        <label>Code: </label>
                        <input></input>
                    </div>
                    <div className='mb-[10px]'>
                        <label>Name: </label>
                        <input></input>
                    </div>
                </div>
            </div>
        </>
    )
}