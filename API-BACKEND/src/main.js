require('dotenv').config()
const express = require('express');
const cors = require('cors')
const db_connection = require('./config/db_connection');
const router = require('./routes/index');

const app = express();
require("../src/models/Roles");
require("../src/models/Users");
require("../src/models/Posts");

app.use(cors())
app.use(express.json())

db_connection.sync({ alter: true })
  .then(() => console.log("Banco sincronizado com sucesso!"))
  .catch((err) => console.error("Erro ao sincronizar:", err));

app.listen(process.env.PORT || 3000, () => {
    console.log(`Servidor rodando em http://localhost: ${process.env.PORT}`);
});


app.use(router)
