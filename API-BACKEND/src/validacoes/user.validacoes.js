const User = require("../models/Users")
const { Op } = require("sequelize");



// const validarUsuarioCadastrado = async (email, username) =>{
//     const usuarioCadastradoByUsername = await User.findOne({ where: { username } });
//     const usuarioCadastradoByEmail = await User.findOne({ where: { email } });

//     if(usuarioCadastradoByEmail || usuarioCadastradoByUsername){
//         return true;
//     }
//     return false;

// }

// -----  FUNCAO Não PERFORMATICA ----- 

const validarUsuarioCadastrado = async (email, username) =>{

    if (!email || !username) return false;

    const usuario = await User.findOne({
        where: {
        [Op.or]: [
            { username },
            { email }
        ]
        }
    })

    return !!usuario
}
module.exports = {
    validarUsuarioCadastrado
}