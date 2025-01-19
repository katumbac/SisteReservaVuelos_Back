# SisteReservaVuelos_Back

## Requerimientos mínimos de la computadora
* Procesador de 2.80GHz
* Memoria RAM de 8GB

## Programas requeridos

  | Programa | Versión |
  |----------|---------|
  | Visual Studio Code | 1.96.0 |
  | MySQL | 8.0.34 |

## Lenguajes Requeridos

  | Lenguaje | Versión |
  |----------|---------|
  | Python| 3.12.2 |

## Frameworks a utilizar
* Django 

## Despliegue del backend
1. Clonamos el repositorio en nuestro computador, para ello necesitamos el URL del repositorio donde se encuentra el código con el backend. Abrimos la consola y copiamos la siguiente instrucción.
   
```markdown
git clone <url del repositorio>
```

2. Una vez clonado el repositorio, abrimos la carpeta en Visual Studio Code.


## Instalación de paquetes necesarios
1.	Abrimos la consola y verificamos si el gestor de paquetes para Python, pip ya está instalado mediante el comando:

```markdown
 pip --version
```

2.	Nos dirigimos de nuevo a Visual Studio Code y abrimos la terminal de este.
3.	Creamos un entorno virtual a través del siguiente comando:
 ```markdown
 python3.12 -m venv nombre_del_entorno
```
4.	Iniciamos el entorno virtual usando el siguiente comando:
 ```markdown
.\nombre_del_entorno\Scripts\Activate
```

5.	Una vez activado el entorno virtual, los paquetes que se requieren ya se encuentran en el repositorio, estos se encuentran en el repo requirementsAct24.txt Para instalar estos paquetes en nuestro entorno virtual usamos el siguiente comando:

```markdown
pip install -r requirements.txt
```

6.	Realizamos las migraciones:
   
```markdown
python manage.py makemigrations
python manage.py migrate
```
6.	Cargamos los datos:
   
```markdown
python manage.py loaddata data.json
```

7. Ejecutamos
```markdown
python manage.py runserver
```
8. Probamos los endpoint en postman


