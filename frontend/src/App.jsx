import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
// import './App.css'
import ChatsPage from './components/ChatsPage';
import Login from "./components/Login";
import Profile from "./components/Profile";
import Registration from "./components/Registration";
import TopNav from "./components/TopNav";
import { AuthProvider, useAuth } from "./context/auth";
import { UserProvider } from "./context/user";
import Homepage from "./components/Homepage";

const queryClient = new QueryClient();

function NotFound() {
  return <h1 className='text-5xl'>404: not found</h1>;
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        logged in: {isLoggedIn.toString()}
      </div>
    </div>
  );
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
      <Route path="/" element={<Navigate to="/chats" />} />
      <Route path="/chats" element={<ChatsPage />} />
      <Route path="/chats/:chatId" element={<ChatsPage />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/" />} />

  </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
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

function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-gray-700 text-white",
    "flex flex-col",
  ].join(" ");
  // <div className='bg-white flex flex-col mx-auto max-w-3xl text-black'>

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <div className='backdrop-blur-3xl bg-white/30	 flex flex-col mx-auto max-w-3xl text-black p-5 gap-5'>
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