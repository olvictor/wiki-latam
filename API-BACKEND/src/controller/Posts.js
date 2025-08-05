const Post = require('../models/Posts')


const cadastrarPost = async (req,res) =>{
    const {title,content} = req.body
    const user = req.usuario

    try{
        await Post.create({
            title,
            content: JSON.stringify(content),
            user_id: user.id
        })
    
        res.status(200).json("aaa")
    
    }catch(err){
        console.log(err.message)
        res.status(500).json({
            mensagem:"erro interno do servidor."
        })
    }
}


module.exports = {
    cadastrarPost
}