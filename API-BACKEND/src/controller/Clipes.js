const Clipes = require('../models/Posts')

const cadastrarClipes = async(req,res)=>{
    const{link} = req.body
    
    try{
        const Clipe = await Clipes.create({link})
        return res.status(201).json({
            success: true,
            message: "Clipe cadastrado com sucesso.",
        })
    } catch(err) {
        return res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }
}


module.exports = {
    cadastrarClipes
}