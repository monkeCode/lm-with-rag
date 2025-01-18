import logo from './logo.svg';
import {Routes, Route, BrowserRouter} from "react-router-dom"
import './App.css';
import {LoginPage, RegisterPage} from "./components/Login"
import ChatPage from './components/ChatPage';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />}/>
          <Route path="/register" element={<RegisterPage />}/>
          <Route path="/chat/:id" element={<ChatPage />}/>
          <Route path="/chat/" element={<ChatPage />}/>
          <Route exact path="/" element={ <p>test</p>}/>
        </Routes>
      </BrowserRouter>
  );
}

export default App;
