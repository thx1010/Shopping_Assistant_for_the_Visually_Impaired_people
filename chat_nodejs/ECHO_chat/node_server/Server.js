
//web socket server

const SocketServer = require('websocket').server
const http = require('http')
const { json } = require('express')

const server = http.createServer((req, res) => {})

server.listen(3000, ()=>{
    console.log("Listening on port 3000...")
})


const Pythonshell = require('python-shell');
let pyshell = new Pythonshell.PythonShell("chat.py");


wsServer = new SocketServer({httpServer:server})
var jsonOBJ;
const connections = []
wsServer.on('request', (req) => {
    const connection = req.accept()
    console.log('new connection')
    connections.push(connection) 

    connection.on("message", (mes) => {
        function getData() {
            return new Promise(function() {
                jsonOBJ = JSON.parse(mes.utf8Data);
                console.log(jsonOBJ["message"]);
                pyshell.send(jsonOBJ["message"]);
                pyshell.on("message", function (message) {
                    console.log(message)
                    connection.send(message)
                });
            });
        }
        
        getData().then(function() {
            pyshell.end(function (err,code,signal) {
                if (err) throw err;
                console.log('finished');
            });
        });
    })

    connection.on('close', (resCode, des) => {
        console.log('connection closed')
        connections.splice(connections.indexOf(connection), 1)
    })

})



