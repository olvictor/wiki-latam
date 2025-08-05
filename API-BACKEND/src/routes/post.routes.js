const express = require('express');
const { cadastrarPost, buscarPosts, buscarPostsPorId } = require('../controller/Posts');
const { validarLogin } = require('../middleware/auth');
const app = express.Router();





posts = app.get('/',buscarPosts)
posts = app.get('/:id',buscarPostsPorId)

app.use(validarLogin)
posts = app.post('/create',cadastrarPost)


module.exports = posts;