const express = require('express');
const auth = express.Router();


auth.post('/auth/register', async(req,res)=>{
    res.send("testando")
});



module.exports = auth