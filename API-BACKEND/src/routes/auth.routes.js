const express = require('express');
const auth = express.Router();
const { cadastrarUsuario,loginUsuario } = require('../controller/User');


auth.post('/register',cadastrarUsuario);
auth.post('/login',loginUsuario)


module.exports = auth