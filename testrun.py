from Cheetah.Template import Template

definition = """Hello, $user firstName.
Your order (#$order id) has shipped:"""
print Template(definition, searchList=[{'user' : "dummyUser",'order' : "dummyOrder"}])
