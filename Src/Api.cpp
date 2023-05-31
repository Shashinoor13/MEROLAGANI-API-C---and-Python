#include <iostream>
#include <string>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fstream>
#include <filesystem>

const int BUFFER_SIZE = 4096;
const int PORT = 8888;

std::string read()
{
    std::fstream fs;
    fs.open("./JSON/shares.json", std::ios::in);
    if (!fs)
    {
        std::cerr << "No Such File Found" << std::endl;
        return "NULL";
    }
    char ch;
    std::string response;
    while (true)
    {
        fs >> ch;
        if (fs.eof())
        {
            break;
        }
        response += ch;
    }
    fs.close();
    return response;
}

std::string getResponse()
{
    std::string data = read();
    std::string response = "HTTP/1.1 200 OK\r\n"
                           "Content-Type:application/json \r\n"
                           "Content-Length: " +
                           std::to_string(data.length()) + "\r\n\r\n" +
                           data;
    return response;
}

int ApiService()
{
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;

    // Generate Response
    std::string response = getResponse();

    // Creating a new socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == -1)
    {
        std::cerr << "Failed To Create Socket." << std::endl;
        return 1;
    }

    // Make use of sockaddr_in
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(PORT);

    // Binding the Socket
    if (bind(serverSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0)
    {
        std::cerr << "Failed To bind." << std::endl;
        return 1;
    }

    // Listen
    listen(serverSocket, 3);

    std::cout << "Server listening on port: " << PORT << std::endl;
    std::cout << "http://localhost:" << 8888 << std::endl;
    while (true)
    {
        // Accept incommin Connections
        int cilentAddressLength = sizeof(clientAddress);
        clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddress, (socklen_t *)&cilentAddressLength);
        if (clientSocket < 0)
        {
            std::cerr << "Failed To Accept Connection" << std::endl;
            return 1;
        }

        // Send Response
        ssize_t bytesWritten = write(clientSocket, response.c_str(), response.length());
        if (bytesWritten < 0)
        {
            std::cerr << "Failed To Write To Socket" << std::endl;
            return 1;
        }
        // close the Socket
        close(clientSocket);
    }
    close(serverSocket);
    return 0;
}