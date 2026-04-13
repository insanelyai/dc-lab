import Pyro4


@Pyro4.expose
class Hello:

   def sayHello(self, name, uin):
       return "Hello " + name + " " + uin + " from CORBA server!"


daemon = Pyro4.Daemon()

uri = daemon.register(Hello)


print("Server is running...")
print("Copy this URI:", uri)

daemon.requestLoop()
