package main

import (
	"fmt"
	"net"
	"time"
)

func _error(panduan int8) {
	if panduan == 1 {
		fmt.Println("连接错误")
	} else if panduan == 2 {
		fmt.Println("发送错误")
	} else if panduan == 3 {
		fmt.Println("接收错误")
	}
}

func Accecpmessage(SocketPort net.Conn) {
	response := make([]byte, 2048)
	messaqe, err := SocketPort.Read(response)
	if err != nil {
		_error(3)
		return
	}
	fmt.Println(string(response[:messaqe]))
}

func SeedMessage(socketprot net.Conn, Message string) {
	_, err := socketprot.Write([]byte(Message))
	if err != nil {
		_error(2)
	}
}

func SocketConnect() (net.Conn, error) {
	address := "127.0.0.1:990"
	conn, err := net.Dial("tcp", address)
	if err != nil {
		_error(1)
		return nil, err
	}
	return conn, nil
}

func main() {
	conn, err := SocketConnect()
	for {
		var needmessage string
		fmt.Println("请输入需要发送的信息")
		fmt.Scanln(&needmessage)
		if needmessage == "exit" {
			break
		}
		if err != nil {
			_error(1)
			continue
		}
		go SeedMessage(conn, needmessage)
		go Accecpmessage(conn)
		time.Sleep(2 * time.Second)
	}
	defer conn.Close()
}
