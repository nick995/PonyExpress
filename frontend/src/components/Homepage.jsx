import { Link, useNavigate } from "react-router-dom";
import Button from "./Button";

function Homepage(){
    return(
        <div className="mx-auto max-w-2xl text-center bg-white">
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl py-4">Welcome to pony express</h1>

            <p className="mt-2 text-sm font-semibold text-gray-400">
            Saddle up, partner! Welcome to Pony Express Chat, where we gallop through conversations with the speed and charm of the legendary Pony Express riders.            </p>            
            <LoginLink/>
        </div>
    )
}

function LoginLink(){
    return (
        <div className="pt-8 flex flex-col">
          <div className="text-xs">
            Want to join?
          </div>
          <Link to="/login">
            <Button className="mt-1 w-full">
              login
            </Button>
          </Link>
        </div>
      );
}

export default Homepage;