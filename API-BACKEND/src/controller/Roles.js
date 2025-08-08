const Role = require("../models/Roles");

const createRole = async(req,res)=>{
   const {name} = req.body

   try{
      const role = await Role.create({ name: name });
      return res.status(201).json({
         success: true,
         message: "Role criada com sucesso.",
         data: role
      })
   } catch(error) {
      console.log(error)
      
      if (error.name === 'SequelizeValidationError') {
         const validationErrors = error.errors.map(err => ({
            field: err.path,
            message: err.message
         }));
         
         return res.status(400).json({
            success: false,
            message: "Erro de validação",
            errors: validationErrors
         });
      }
      
      if (error.name === 'SequelizeUniqueConstraintError') {
         const validationErrors = error.errors.map(err => ({
            field: err.path,
            message: err.message
         }));
         
         return res.status(400).json({
            success: false,
            message: "Erro de validação",
            errors: validationErrors
         });
      }
      
      return res.status(500).json({
         success: false,
         message: "Problema interno do servidor."
      })
   }   
}


module.exports = {
    createRole
}