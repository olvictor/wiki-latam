const express = require('express');
const { cadastrarClipes, buscarClipes } = require('../controller/Clipes');
const app = express.Router();



clipes = app.post('/create',cadastrarClipes)
clipes = app.get('/find',buscarClipes)

module.exports = clipes