// const Post = require('../models/Posts')
const { Post, User } = require("../models/index");

const cadastrarPost = async (req,res) =>{
    const {title,content} = req.body
    const user = req.usuario

    try{
        const novoPost = await Post.create({
            title,
            content,
            user_id: user.id
        })
    
        return res.status(201).json({
            success: true,
            data: {
                id: novoPost.id,
                title: novoPost.title,
                content: novoPost.content,
                user_id: novoPost.user_id,
                createdAt: novoPost.createdAt
            },
            message: "Post criado com sucesso"
        })
    
    }catch(err){
        console.log(err.message)
        
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
        
        res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }
}

const buscarPosts = async(req,res)=>{
    const { user_id } = req.query;

    console.log(user_id)
    try {
        if(user_id){
        const posts = await Post.findAll({
        where: { user_id },
        include: {
            model: User,
            attributes: ["id", "username", "email","img_url"]
        }
        });
        return res.status(200).json({
            success: true,
            data: posts,
            message: "Posts recuperados com sucesso"
        });
        }


        const posts = await Post.findAll({include: {
            model: User,
            attributes: ["id", "username", "email"]
        }});
        return res.status(200).json({
            success: true,
            data: posts,
            message: "Posts recuperados com sucesso"
        });
    } catch (err) {
        console.log(err.message);
        return res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        });
    }
}


const buscarPostsPorId = async(req,res) =>{
    const {id} = req.params
    
    if (!id) {
        return res.status(400).json({
            success: false,
            message: "Erro de validação",
            errors: [{
                field: "id",
                message: "O parâmetro id é obrigatório."
            }]
        })
    }

    try {
        const post = await Post.findByPk(id)
        
        if (!post) {
            return res.status(404).json({
                success: false,
                message: "Post não encontrado"
            })
        }

        return res.status(200).json({
            success: true,
            data: post,
            message: "Post recuperado com sucesso"
        })
    } catch (err) {
        console.log(err.message)
        return res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }
}

module.exports = {
    cadastrarPost,
    buscarPosts,
    buscarPostsPorId,
    
}