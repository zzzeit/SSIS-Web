

export default async function updateTableData() {
    const [table_data, set_table_data] = useState([]);

        console.log(`Fetching Data...`);
        const data = await fetch('http://192.168.1.50:5000/get/colleges');
        const result = await data.json();
        set_table_data(result);
    };
}