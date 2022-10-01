module.exports = (app) => {
  console.log("2 merkle exports")
  const merkle = require('../../controllers/merkle.controller.js')
  var router = require('express').Router()
  // merkle
  console.log("6 merkle exports")
  router.post('/', merkle.proof)
  console.log("8 merkle exports")

  app.use('/api/v1/merkle', router)
}