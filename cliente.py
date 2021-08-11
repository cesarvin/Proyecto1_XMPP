import sys

while True: 
  print("\nMenu pruncipal\n\t1. Registrar una nueva cuenta en el servidor\n\t2. Iniciar sesión con una cuenta\n\t3. Eliminar la cuenta del servidor\n\t4. Salir")
  op = int(input())

  # validate selected option
  if (op < 1 and op > 4):
    print('Seleccione una opcion valida')

  # register a new account on the server
  if (op==1):
    pass 
  
  # log in with an account on the server
  if (op==2):
    pass 
  
  # delete an account
  if (op==3):
    pass 

  # exit
  if (op==4):
    sys.exit()