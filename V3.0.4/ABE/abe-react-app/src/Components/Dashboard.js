import './index.css';

function Dashboard() {
  return (
  <div id="bodyDiv" class="flex items-center justify-center h-screen bg-discord-gray text-white flex-col">
    <div class="text-2xl">Welcome to the dashboard,</div>
      <div class="text-4xl mt-3 flex items-center font-medium" >
        <img src='' id="avatar" class="rounded-full w-12 h-12 mr-3"/>
        <div id="name"></div>
      </div>
    <a href="/" class="text-sm mt-5">Logout</a>
  </div>
  );
}

export default Dashboard;
