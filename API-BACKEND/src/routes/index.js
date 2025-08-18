const express = require("express");
const router = express.Router();


const rolesRoutes = require("./role.routes");
const authRoutes = require("./auth.routes");
const postsRoutes = require('./post.routes')
const clipesRoutes = require('./clips.routes')
router.use('/clipes',clipesRoutes)
router.use('/role',rolesRoutes);
router.use('/auth',authRoutes);
router.use('/posts',postsRoutes)



module.exports = router;