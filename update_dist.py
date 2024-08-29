import subprocess

# Define los comandos que deseas ejecutar
comando1 = "python setup.py sdist bdist_wheel"
comando2 = "twine upload dist/*"

# Ejecuta el primer comando
resultado1 = subprocess.run(comando1, shell=True, capture_output=True, text=True)
print(f"Salida del primer comando: {resultado1.stdout}")

# Ejecuta el segundo comando
resultado2 = subprocess.run(comando2, shell=True, capture_output=True, text=True)
print(f"Salida del segundo comando: {resultado2.stdout}")