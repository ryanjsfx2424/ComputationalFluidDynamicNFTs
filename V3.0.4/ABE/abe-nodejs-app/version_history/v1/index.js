const path = require('path');
const express = require('express');
const ejs = require('ejs');

const app = express();

app.use('',express.static(path.join(__dirname, 'public')));

app.get('/', (request, response) => {
	return response.sendFile('index.html', { root: '.' });
});

app.get('/auth/discord', (request, response) => {
	return response.sendFile('dashboard.html', { root: '.' });
});

app.get('/dashboard/:guildId', (request, response) => {
	console.log("18 request.params: ", request.params);
	return response.sendFile('settings.html', { root: '.' });
});

const port = '3000';
app.listen(port, () => console.log(`App listening at http://localhost:${port}`));
