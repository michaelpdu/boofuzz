#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#define MAX 80 
#define PORT 8901 
#define SA struct sockaddr 

// Function designed for chat between client and server. 
void func(int sockfd) 
{ 
    char buff[MAX]; 
    // infinite loop for chat 
    for (;;) { 
        bzero(buff, MAX); 
        // read the message from client and copy it in buffer 
        int size = read(sockfd, buff, sizeof(buff)); 
        printf("Input buffer size is %d\n", size);
        if (size == 0) break;
        if (size >= 50) {
            printf("trigger crash here.");
            char *mem = NULL;
            *mem = 0x41414141; 
        }
        printf("From client: %s\n", buff);
    } 
} 

// Driver function 
int main() 
{ 
    int sockfd, connfd, len; 
    struct sockaddr_in servaddr, cli; 

    // socket create and verification 
    sockfd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sockfd == -1) { 
        printf("socket creation failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully created..\n"); 
    bzero(&servaddr, sizeof(servaddr)); 

    // assign IP, PORT 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
    servaddr.sin_port = htons(PORT); 

    // Binding newly created socket to given IP and verification 
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
        printf("socket bind failed...\n"); 
        exit(0); 
    } 
    else
        printf("Socket successfully binded..\n"); 

    // Now server is ready to listen and verification 
    if ((listen(sockfd, 5)) != 0) { 
        printf("Listen failed...\n"); 
        exit(0); 
    } 
    else
        printf("Server listening at port 8901..\n"); 
    len = sizeof(cli); 

    // Accept the data packet from client and verification 
    connfd = accept(sockfd, (SA*)&cli, &len); 
    if (connfd < 0) { 
        printf("server acccept failed...\n"); 
        exit(0); 
    } 
    else
        printf("server acccept the client...\n"); 

    // Function for chatting between client and server 
    func(connfd); 

    // After chatting close the socket 
    close(sockfd); 

    //

    fd_set rd;
    struct timeval tv;
    int err;
    
    FD_ZERO(&rd);
    FD_SET(0,&rd);
    
    tv.tv_sec = 10;
    tv.tv_usec = 0;
    err = select(1,&rd,NULL,NULL,&tv);
    
    if(err == 0) //超时
    {
        printf("select time out!\n");
    }
    else if(err == -1)  //失败
    {
        printf("fail to select!\n");
    }
    else  //成功
    {
        printf("data is available!\n");
    }

} 

