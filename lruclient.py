import xmlrpclib

# SImple client to test your lruserver, remember to change localhost and port to your needs
proxy = xmlrpclib.ServerProxy("http://localhost:8080/")

while True:
    print "Select an option:\n1.-Get a value from the server.\n2.-Put a value into the server."
    option = raw_input("? ")
    if option != "1" and option != "2":
        print "Not a valid option!"
        continue
    key = raw_input("Type a Key: ")    
    if option == "1":
        print "(Key, Value) ==> (%s, %s)" % (key, proxy.get(key))
    else:
        value = raw_input("Type a Value: ")
        proxy.put(key, value)    
