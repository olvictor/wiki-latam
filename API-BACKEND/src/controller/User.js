const express = require('express');
const User = require('../models/Users');
const bcrypt = require('bcrypt');
const Role = require('../models/Roles');
const {validarUsuarioCadastrado} = require('../validacoes/user.validacoes');
const private_key = process.env.PRIVATE_kEY;
const jwt = require('jsonwebtoken')


const cadastrarUsuario = async(req,res)=>{
    const { username, password, email, role_id } = req.body

    if( await validarUsuarioCadastrado(email,username)){
        return res.status(400).json({
            success: false,
            message: "Usuário ou Email já cadastrado no sistema.",
            errors: [
                { field: "username/email", message: "Usuário ou Email já cadastrado no sistema." }
            ]
        })
    }

    try{
        const senhaCriptografada = await bcrypt.hash(password,10)
        
        const cadastrarUsuario = await User.create({ 
            username, 
            password_hash: senhaCriptografada,
            email,
            role_id
        });
        const usuario = cadastrarUsuario.get({ plain: true });

        return res.status(201).json({
            success: true,
            message: "Usuário cadastrado com sucesso.",
            data: {
                id: usuario.id,
                username: usuario.username,
                email: usuario.email
            }
        })
    } catch(err) {
        console.log(err.message);
        
        if (err.name === 'SequelizeValidationError') {
            const validationErrors = err.errors.map(error => ({
                field: error.path,
                message: error.message
            }));
            
            return res.status(400).json({
                success: false,
                message: "Erro de validação",
                errors: validationErrors
            });
        }
        
        if (err.name === 'SequelizeUniqueConstraintError') {
            const validationErrors = err.errors.map(error => ({
                field: error.path,
                message: error.message
            }));
            
            return res.status(400).json({
                success: false,
                message: "Erro de validação",
                errors: validationErrors
            });
        }
        
        // Tratamento específico para erro de chave estrangeira (role_id inválido)
        if (err.name === 'SequelizeForeignKeyConstraintError' && err.message.includes('Users_role_id_fkey')) {
            return res.status(400).json({
                success: false,
                message: "Erro de validação",
                errors: [{
                    field: "role_id",
                    message: "Role inválida. A role especificada não existe."
                }]
            });
        }
        
        res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }


}

const loginUsuario = async(req,res)=>{
    const { username, password} = req.body

    if (!username || !password) {
        return res.status(400).json({
            success: false,
            message: "Erro de validação",
            errors: [
                !username ? {field: "username", message: "O campo username é obrigatório."} : null,
                !password ? {field: "password", message: "O campo password é obrigatório."} : null
            ].filter(Boolean)
        })
    }

    try{
        const usuarioCadastrado = await User.findOne({where: {username}});
        
        if(!usuarioCadastrado){
            return res.status(400).json({
                success: false,
                message: "Usuário ou senha inválidos."
            })
        }

        const validarSenha = await bcrypt.compare(password, usuarioCadastrado.dataValues.password_hash)

        if(!validarSenha){
            return res.status(400).json({
                success: false,
                message: "Usuário ou senha inválidos."
            })
        }
        
        var token = jwt.sign({ username }, private_key,{ algorithm: 'HS256', expiresIn: '24h' });

        return res.status(200).json({
            success: true,
            message: "Login realizado com sucesso",
            data: {
                usuario: {
                    username: usuarioCadastrado.dataValues.username,
                    email: usuarioCadastrado.dataValues.email,
                    role_id: usuarioCadastrado.dataValues.role_id,
                },
                token: token
            }
        });
    }catch(err){
        console.log(err.message);
        res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }    
};



const detalharUsuario = async(req,res) =>{
    return res.status(200).json({
        success: true,
        message: "Detalhes do usuário recuperados com sucesso",
        data: {
            usuario: req.usuario
        }
    })
}

const editarUsuario = async(req,res) =>{
        const {id} = req.params
        const dados = req.body   
    

        const usuario = await User.findByPk(id);
 
        if(!usuario){
            return res.status(400).json({
        success: false,
        message: "Acesso negado.",
        })
        }

        if(usuario.dataValues.id != req.usuario.id){
            return res.status(400).json({
        success: false,
        message: "Acesso negado.",
        })
        }


        try{
            if(dados.password){
                const senhaCriptografada = await bcrypt.hash(dados.password,10)
                dados.password_hash = senhaCriptografada;
                delete dados.senha;
            }

            const userUpdate =  await User.update(
                dados,
                  {
                    where: {
                    id: usuario.dataValues.id,
                    },
                },
            );
            return res.status(200).json({
            success: true,
            message: "Dados atualizados com sucesso",
    })
        }catch(error){
            console.log(error.message)
            res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
            })
        }
}
module.exports = {
    cadastrarUsuario,
    loginUsuario,
    detalharUsuario,
    editarUsuario
}