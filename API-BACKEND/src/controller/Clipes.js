const Clipes = require('../models/Clips.js')

const cadastrarClipes = async(req,res)=>{
    const { link }  = req.body
    console.log(link)
    if(!link){
        return res.status(400).json({
            success: false,
            message: "O Campo link é obrigatório.",
        })
    }

    try{
        const Clipe = await Clipes.create({link})
        return res.status(201).json({
            success: true,
            message: "Clipe cadastrado com sucesso.",
        })
    } catch(err) {
        console.log(err.message)
        return res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }
}


const buscarClipes = async (req,res) =>{
    try{
        const clipes = await Clipes.findAll();
        console.log(clipes)
        return res.status(200).json({
            success: true,
            message: "Clipe cadastrado com sucesso.",
            data : clipes
        })
    } catch(err) {
        console.log(err.message)
        return res.status(500).json({
            success: false,
            message: "Erro interno do servidor."
        })
    }
}


module.exports = {
    cadastrarClipes,
    buscarClipes
}