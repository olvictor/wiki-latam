const express = require('express');
const auth = express.Router();
const { cadastrarUsuario,loginUsuario, detalharUsuario, editarUsuario } = require('../controller/User');
const { validarLogin } = require('../middleware/auth');


auth.post('/register',cadastrarUsuario);
auth.post('/login',loginUsuario)

auth.use(validarLogin)

auth.get('/user',detalharUsuario)
auth.put('/edit/:id',editarUsuario)
module.exports = auth