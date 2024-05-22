import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./context/auth";
import { UserProvider } from "./context/user";
import { useAuth } from "./hooks";
import ChatsPage from './components/ChatsPage';
import Login from "./components/Login";
import Profile from "./components/Profile"
import Registration from "./components/Registration";
import TopNav from "./components/TopNav";
import HomePage from './components/HomePage';
import UploadVideosPage from './components/video/UploadVideosPage';
import "./index.css"

const queryClient = new QueryClient();

function NotFound(){
  return <h1>404 Not Found</h1>;
}


function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}


function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/chats" element={<ChatsPage/>} />
      <Route path="/chats/:chatId" element={<ChatsPage />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/error/404" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
      <Route path="/upload_videos" element={<UploadVideosPage />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="max-h-main">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

// function App() {
//   return (
//     <QueryClientProvider client={queryClient}>
//       <BrowserRouter>
//         <div className="bg-slate-700 flex flex-col mx-auto max-w-3xl" >
//           <header>
//             <h1 className="text-center text-2xl font-extrabold py-2">pony express</h1>
//           </header>
//           <main className="px-4">
//             <Routes>
//               <Route path="/" element={<ChatsPage/>} />
//               <Route path="/chats" element={<ChatsPage/>} />
//               <Route path="/chats/:chatId" element={<ChatsPage />} />
//               <Route path="/error/404" element={<NotFound/>} />
//               <Route path="*" element={<Navigate to="error/404"/>} />
//             </Routes>
//           </main>
//         </div>
//       </BrowserRouter> 
//     </QueryClientProvider>
//   );
// }


function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-gray-700 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <div className={className}>
              <Header />
              <Main />
            </div>
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App
