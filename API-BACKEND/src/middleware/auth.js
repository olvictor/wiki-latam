const jwt = require("jsonwebtoken");
const User = require("../models/Users");
const private_key = process.env.PRIVATE_kEY


const validarLogin = async (req,res,next)=>{
    const {authorization} = req.headers;
    if(!authorization){
        return res.status(400).json({mensagem:"Não autorizado"});
        
    }
    const token = authorization.split('Bearer ')[1];

    if (!token) {
        return res.status(400).json({mensagem:"Não autorizado"});
    }

    try {
        const decoded = jwt.verify(token, private_key);

        const usuario = await User.findOne({username: decoded.username})

        req.usuario = {
            id: usuario.dataValues.id,
            username: usuario.dataValues.username,
            email: usuario.dataValues.email,
            role_id: usuario.dataValues.role_id
        } 
        next();
    } catch (err) {
        console.log(err.message)
        return res.status(403).json({ error: 'Token inválido!' });
    }

}



module.exports = {
    validarLogin
}