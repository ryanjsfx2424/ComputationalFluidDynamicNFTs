import './index.css';

function Login() {
  return (
    <div class="flex items-center justify-center h-screen bg-discord-gray text-white" >
        <a id="login" href="https://discord.com/api/oauth2/authorize?client_id=1018491238703431780&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth%2Fdiscord&response_type=token&scope=identify%20guilds" class="bg-discord-blue  text-xl px-5 py-3 rounded-md font-bold flex items-center space-x-4 hover:bg-gray-600 transition duration-75">
            <i class="fa-brands fa-discord text-2xl"></i>
            <span>Login with Discord</span>
        </a>
    </div>
  );
}

export default Login;
