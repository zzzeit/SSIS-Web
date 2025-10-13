

export default function Button({children, className, ascending}) {
    if (ascending) {
        return (
            <>
                <button className={className}>
                    {children}
                </button>
            </>
        );      
    }

    return (
        <>
            <button className={className}>
                <span style={{transform: 'scaleY(-1)'}}>
                    {children}
                </span>

            </button>
        </>
    );
}