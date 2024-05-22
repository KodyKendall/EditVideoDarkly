import { useAuth } from "../hooks";
import { Navigate } from 'react-router-dom';
import WelcomeCard from "./WelcomCard";

function HomePage() {
    const { isLoggedIn, logout } = useAuth();
  
    if(isLoggedIn){
        return (<Navigate to="/chats" />);
    }
    return (
        <WelcomeCard></WelcomeCard>
    );
  }

  export default HomePage;