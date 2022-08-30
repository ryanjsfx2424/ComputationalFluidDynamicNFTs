const express = require('express')
const cors = require('cors')
const app = express()
const port = process.env.PORT || 3001

// implement cors
app.use(cors())

app.use(express.json())

// Routes
app.get('/', (req, res) => {
  res.send('Welcome to RDH backend!')
})

require('./app/routes/v1/merkle.route')(app)

app.listen(port, () => {
  console.log(`Server app listening on port ${port}`)
})
