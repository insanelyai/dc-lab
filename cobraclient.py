import Pyro4

uri = input("Paste URI here:")

hello = Pyro4.Proxy(uri)

name = input("Enter your name:")
uin = input("Enter your uin:")

print(hello.sayHello(name, uin))
