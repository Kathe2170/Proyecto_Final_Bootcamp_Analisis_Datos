def suma_uno():

    n1 = int(input("Digite un número: "))
    n2 = int(input("Digite un número: "))

    resultado = n1 + n2
    print("El resultado de la suma es ", resultado)

suma_uno()

def suma_notas():
    nota1 = float(input("Digite la nota: "))
    nota2 = float(input("Digite la nota: "))
    nota3 = float(input("Digite la nota: "))
    nota4 = float(input("Digite la nota: "))

    promedio = (nota1 + nota2 + nota3 + nota4)/4
    print("El promedio es: ", promedio)

suma_notas()