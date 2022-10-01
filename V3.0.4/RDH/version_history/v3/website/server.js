const express = require('express')
const cors = require('cors')
const path = require('path')
const app = express()
//const port = process.env.PORT || 3001
const port = 3001

// implement cors
app.use(cors())

app.use(express.json())

// Routes
app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, './client/build', 'index.html'))
})

require('./app/routes/v1/merkle.route')(app)

app.listen(port, () => {
  console.log(`Server app listening on port ${port}`)
})
