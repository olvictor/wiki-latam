const express = require('express');
const auth = express.Router();

const { cadastrarUsuario } = require('../controller/User');


auth.post('/register', cadastrarUsuario);

module.exports = auth