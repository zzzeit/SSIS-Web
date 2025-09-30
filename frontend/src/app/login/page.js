import './Login.css'

export default function Login() {

    return (
        <>
            <div className="my-div h-screen flex items-center justify-center">
                <div className="login-div h-80 max-w-300 min-w-100">


                    <form action="/login" method="post" className='my-form'>
                        <div className='mt-20'>
                            <label htmlFor="username">Username:</label>
                            <input type="text" id="username" name="username" required /><br />
                        </div>
                        <div>
                            <label htmlFor="password">Password:</label>
                            <input type="password" id="password" name="password" required /><br />                          
                        </div>
                        
                        <button type="submit" className=''>Login</button>
                    </form>



                </div>
            </div>
        </>
    );
}