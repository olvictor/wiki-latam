const Post = require('../models/Posts')
const { post } = require('../routes')


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

const buscarPosts = async(req,res)=>{
    const posts = await Post.findAll();

    res.status(200).json(posts);

}


const buscarPostsPorId = async(req,res) =>{
    const {id} = req.params
    const post = await Post.findByPk(id)

    return res.status(200).json(post)
}
module.exports = {
    cadastrarPost,
    buscarPosts,
    buscarPostsPorId
}