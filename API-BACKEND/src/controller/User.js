const express = require('express');
const User = require('../models/Users');
const auth = express.Router();
const bcrypt = require('bcrypt');
const Role = require('../models/Roles');
const {validarUsuarioCadastrado} = require('../validacoes/user.validacoes')



const cadastrarUsuario = async(req,res)=>{
    const { username, password, email , role_id} = req.body

    if( await validarUsuarioCadastrado(email,username)){
        return res.status(400).json({
            "mensagem": "Usuário ou Email já cadastrado no sistema."
        })
    }

    const senhaCriptografada = await bcrypt.hash(password,10)
    
    const cadastrarUsuario = await User.create({ username, password_hash: senhaCriptografada,email,role_id});
    const usuario = cadastrarUsuario.get({ plain: true });

    return res.status(201).json({
        mensagem:"Usuário cadastrado com sucesso.",
        usuario: {
            id: usuario.id,
            username: usuario.username,
            email: usuario.email
        }
    })
}


module.exports = {
    cadastrarUsuario
}