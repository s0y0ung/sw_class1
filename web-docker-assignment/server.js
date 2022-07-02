const express = require("express")
const app = express()
var router = require('./router/main')(app);

app.use(express.static("public"))

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

const server = require("http").createServer({}, app)

server.listen(3000, function(){
    console.log("HTTP를 포트 3000에 오픈합니다")
})