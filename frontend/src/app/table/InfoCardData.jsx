import './InfoCard.css'

export default function InfoCardData({text='Label: ', value='None'}) {

    return (
        <>
            <div className='info-card-data'>
                <label>{text}</label>
                <input value={value} readOnly />
            </div>
        </>
    );
}