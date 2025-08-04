const jwt = require("jsonwebtoken")
const private_key = process.env.PRIVATE_kEY


const validarLogin = (req,res)=>{
    const {authorization} = req.headers;
    if(!authorization){
        return res.status(400).json({mensagem:"Não autorizado"});
        
    }
    const token = authorization.split('Bearer ')[1];

    if (!token) {
        return res.status(400).json({mensagem:"Não autorizado"});
    }
    try {
        const decoded = jwt.verify(token, private_key,);
        req.user = decoded; 
        next();
    } catch (err) {
        return res.status(403).json({ error: 'Token inválido!' });
    }

}



module.exports = {
    validarLogin
}