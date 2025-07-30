const Role = require("../models/Roles");


const createRole = async(req,res)=>{
   const {name} = req.body
   if(!name) {
     return res.status(400).json({mensagem:"O campo name é obrigatório."})
   }

   try{
      const role = await Role.create({ name: name });
      return  res.status(201).json({
         mensagem: "Role criada com sucesso.",
         role
      })
   }catch(error){
      console.log(error)
      return res.status(500).json({
         mensagem: "Problema interno do servidor.",
      })
   }   
}


module.exports = {
    createRole
}