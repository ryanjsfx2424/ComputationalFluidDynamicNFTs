import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div class="flex items-center justify-center h-screen bg-discord-gray text-white" >
        <a id="login" href="#discord_token_link" class="bg-discord-blue  text-xl px-5 py-3 rounded-md font-bold flex items-center space-x-4 hover:bg-gray-600 transition duration-75">
            <i class="fa-brands fa-discord text-2xl"></i>
            <span>Login with Discord</span>
        </a>
    </div>
  );
}

export default App;
