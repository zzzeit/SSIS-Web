import Image from "next/image";

function UCG() {
    return(
            <Image className="ml-auto mr-auto pt-56" src="/under-construction.gif" width={300} height={500} unoptimized={true} alt='under construction' />
    );
}

export default UCG;