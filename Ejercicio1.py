
datos = {"documento":1000000, "nombre":"Ana", "edad":22}
datos["celular"] = 3209395996

# for c,v in datos.items():
#     print(c, " ", v)

basedatos = {1:{"documento":1000000, "nombre":"Ana", "edad":22},
            2:{"documento":1000045, "nombre":"Maria", "edad":10},
            3:{"documento":1003572, "nombre":"Juan", "edad":25}
            }

# Mostrar los nombres del diccionario

# for c,v in basedatos.items():
#     print(v["nombre"])

# Mostrar el nombre de las personas que sean menores de edad.

for c,v in basedatos.items():
    if v["edad"] > 18:
        print(v["nombre"])