const express = require('express');
const User = require('../models/Users');
const auth = express.Router();
const bcrypt = require('bcrypt');
const Role = require('../models/Roles');
const {validarUsuarioCadastrado} = require('../validacoes/user.validacoes');
const private_key = process.env.PRIVATE_kEY;
const jwt = require('jsonwebtoken')


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

const loginUsuario = async(req,res)=>{
    const { username, password} = req.body

    const usuarioCadastrado = await User.findOne({username});

    const validarSenha = await bcrypt.compare(password,usuarioCadastrado.dataValues.password_hash)

    if(!usuarioCadastrado || !validarSenha){
        return res.status(400).json({
            mensagem:"usário ou senha inválidos."
        })
    }
    var token = jwt.sign({ username }, private_key,{ algorithm: 'HS256', expiresIn: '24h' });

    return res.json({
        token
    });
};

module.exports = {
    cadastrarUsuario,
    loginUsuario
}