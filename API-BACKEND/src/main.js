const express = require('express')

const app = express();

app.listen(4000, () => {
    console.log(`🚀 Servidor rodando em http://localhost:`);
});


app.get('/',async(req,res)=>{
    res.json({messagem:"testando"})
}) 