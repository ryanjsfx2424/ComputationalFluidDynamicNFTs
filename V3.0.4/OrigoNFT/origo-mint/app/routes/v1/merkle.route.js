module.exports = (app) => {
  const merkle = require('../../controllers/merkle.controller.js')
  var router = require('express').Router()
  // merkle
  router.post('/', merkle.proof)

  app.use('/api/v1/merkle', router)
}
