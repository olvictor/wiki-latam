const express = require('express');
const { cadastrarClipes } = require('../controller/Clipes');
const app = express.Router();



clipes = app.post('/create',cadastrarClipes)


module.exports = clipes