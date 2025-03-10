const net = require('net');

let clientSocket = null;
const server_port = 65432;
const server_addr = "192.168.86.38";   // the IP address of your Raspberry PI

function getClientSocket() {
    if (!clientSocket || clientSocket.destroyed) {
        clientSocket = net.createConnection({ port: server_port, host: server_addr }, () => {
            console.log('Connected to server!');
        });

        clientSocket.on('data', (data) => {
            document.getElementById("greet_from_server").innerHTML = data;
            console.log(data.toString());
        });

        clientSocket.on('end', () => {
            console.log('Disconnected from server');
            clientSocket = null;
        });

        clientSocket.on('error', (err) => {
            console.error('Socket error:', err);
            clientSocket = null;
        });
    }
    return clientSocket;
}

function client(input){
    
    const net = require('net');
    //var input = document.getElementById("myName").value;

    const socket = getClientSocket();
    socket.write(`${input}`);    
}

function greeting(){

    // get the element from html
    var name = document.getElementById("myName").value;
    // update the content in html
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    // send the data to the server 
    to_server(name);
    client();

}
