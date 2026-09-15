# Monolito FastAPI con Vagrant, VirtualBox y Ansible

Proyecto educativo para desplegar una aplicación monolítica desarrollada con **FastAPI** dentro de una máquina virtual Ubuntu utilizando **Vagrant**, **VirtualBox** y **Ansible**.

La aplicación contiene tres módulos funcionales:

* Users
* Orders
* Payments

Todos forman parte de **una única aplicación FastAPI**, ejecutada como un único proceso y expuesta por el puerto `8000`.

---

## 1. Arquitectura

La arquitectura del proyecto es:

```text
                         Mac
                          │
              ┌───────────┴───────────┐
              │                       │
           Vagrant                VirtualBox
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                  Ubuntu Virtual Machine
                          │
                       Ansible
                          │
                          ▼
                 monolith.service
                          │
                          ▼
                    FastAPI :8000
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
           Users        Orders       Payments
```

Los tres módulos están dentro de la misma aplicación.

No existen tres servidores independientes.

---

## 2. Monolito vs microservicios

En este proyecto:

```text
                 MONOLITO

              FastAPI :8000
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Users      Orders     Payments
```

Existe:

* Una aplicación
* Un proceso
* Un puerto
* Un servicio systemd
* Un entorno virtual de Python

En una arquitectura de microservicios tendríamos:

```text
Users       → :8001
Orders      → :8002
Payments    → :8003
```

Cada servicio tendría su propio proceso y servicio systemd.

---

## 3. Objetivo del proyecto

El objetivo es aprender cómo:

1. Crear una máquina virtual con Vagrant.
2. Utilizar VirtualBox como proveedor.
3. Configurar automáticamente Ubuntu con Ansible.
4. Crear un entorno virtual de Python.
5. Instalar FastAPI y Uvicorn.
6. Desplegar una aplicación web.
7. Utilizar systemd para administrar la aplicación.
8. Acceder a la aplicación desde el sistema operativo anfitrión.
9. Entender la diferencia entre una arquitectura monolítica y una arquitectura basada en microservicios.

---

## 4. Tecnologías utilizadas

| Tecnología | Función                                |
| ---------- | -------------------------------------- |
| macOS      | Sistema operativo anfitrión            |
| VirtualBox | Ejecuta la máquina virtual             |
| Vagrant    | Crea y administra la VM                |
| Ubuntu     | Sistema operativo de la VM             |
| Ansible    | Configura automáticamente la VM        |
| Python     | Lenguaje de programación               |
| FastAPI    | Framework para construir la API        |
| Uvicorn    | Servidor ASGI                          |
| systemd    | Administra el proceso de la aplicación |
| Git        | Control de versiones                   |

---

# 5. Requisitos

En el Mac se necesita instalar:

* Git
* VirtualBox
* Vagrant
* Ansible

No es necesario instalar FastAPI ni Uvicorn directamente en macOS.

Estas dependencias se instalarán dentro de la máquina virtual mediante Ansible.

---

# 6. Estructura del proyecto

```text
monolith-vagrant-ansible/
│
├── Vagrantfile
├── README.md
│
├── ansible/
│   └── site.yml
│
├── app/
│   ├── main.py
│   ├── users.py
│   ├── orders.py
│   ├── payments.py
│   └── requirements.txt
│
└── systemd/
    └── monolith.service
```

---

# 7. ¿Qué hace cada componente?

## Vagrant

Vagrant crea y administra la máquina virtual.

Por ejemplo:

```bash
vagrant up
```

crea y arranca la VM.

---

## VirtualBox

VirtualBox es el software que realmente ejecuta la máquina virtual.

La relación es:

```text
Vagrant
   │
   ▼
VirtualBox
   │
   ▼
Ubuntu VM
```

---

## Ansible

Ansible configura Ubuntu automáticamente.

Instala Python, crea el usuario de la aplicación, crea el entorno virtual, copia el código, instala las dependencias y configura systemd.

---

## FastAPI

FastAPI proporciona la API HTTP.

Los endpoints son:

```text
GET /users/{user_id}
GET /orders/{order_id}
GET /payments/{payment_id}
GET /health
```

---

## Uvicorn

Uvicorn ejecuta la aplicación FastAPI:

```text
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## systemd

systemd mantiene la aplicación ejecutándose.

Si la aplicación se detiene, la configuración:

```ini
Restart=always
```

permite que systemd intente reiniciarla.

---

# 8. Clonar el proyecto

Desde el Mac:

```bash
git clone <URL_DEL_REPOSITORIO>
cd monolith-vagrant-ansible
```

---

# 9. Crear la máquina virtual

Desde la raíz del proyecto:

```bash
vagrant up
```

Vagrant realizará aproximadamente este proceso:

```text
Mac
 │
 │ vagrant up
 ▼
Vagrant
 │
 ▼
VirtualBox
 │
 ▼
Ubuntu
 │
 ▼
Ansible
 │
 ├── instala Python
 ├── crea usuario monolith
 ├── crea /opt/monolith
 ├── crea virtualenv
 ├── copia la aplicación
 ├── instala FastAPI y Uvicorn
 ├── instala monolith.service
 └── inicia la aplicación
```

La primera ejecución puede tardar varios minutos porque Vagrant necesita descargar la imagen de Ubuntu.

---

# 10. Verificar que la VM está funcionando

Desde el Mac:

```bash
vagrant status
```

Debería aparecer algo similar a:

```text
default                   running (virtualbox)
```

---

# 11. Entrar a la máquina virtual

```bash
vagrant ssh
```

Ahora estamos dentro de Ubuntu.

El prompt será similar a:

```text
vagrant@monolith:~$
```

---

# 12. Verificar systemd

Dentro de Ubuntu:

```bash
systemctl status monolith
```

Debería aparecer:

```text
Active: active (running)
```

También podemos utilizar:

```bash
systemctl is-active monolith
```

El resultado esperado es:

```text
active
```

---

# 13. Verificar el proceso

Dentro de Ubuntu:

```bash
ps aux | grep uvicorn
```

Deberíamos encontrar un proceso similar a:

```text
/opt/monolith/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 14. Probar la aplicación desde Ubuntu

Dentro de la VM:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{
  "application": "monolith",
  "status": "ok"
}
```

Probar Users:

```bash
curl http://localhost:8000/users/1
```

Probar Orders:

```bash
curl http://localhost:8000/orders/1
```

Probar Payments:

```bash
curl http://localhost:8000/payments/1
```

---

# 15. Probar desde el Mac

Salir de la VM:

```bash
exit
```

Ahora estamos nuevamente en macOS.

Como Vagrant configuró el port forwarding:

```text
Mac :8000
    │
    ▼
VM :8000
```

podemos utilizar:

```bash
curl http://localhost:8000/health
```

También:

```bash
curl http://localhost:8000/users/1
```

```bash
curl http://localhost:8000/orders/1
```

```bash
curl http://localhost:8000/payments/1
```

---

# 16. Swagger

FastAPI genera automáticamente una interfaz Swagger.

Abrir en el navegador:

```text
http://localhost:8000/docs
```

También está disponible:

```text
http://localhost:8000/redoc
```

Desde Swagger podemos probar los diferentes endpoints.

---

# 17. Flujo interno del monolito

En este proyecto no existe comunicación HTTP entre Users, Orders y Payments.

Por ejemplo:

```text
GET /payments/1
       │
       ▼
   get_payment()
       │
       ▼
    get_order()
       │
       ▼
    get_user()
```

Todo ocurre dentro del mismo proceso Python.

Esto es diferente a los microservicios.

En microservicios:

```text
Payments
    │
    │ HTTP
    ▼
Orders
    │
    │ HTTP
    ▼
Users
```

En el monolito:

```text
Payments
    │
    │ llamada de función
    ▼
Orders
    │
    │ llamada de función
    ▼
Users
```

---

# 18. Ver los logs

Dentro de Ubuntu:

```bash
vagrant ssh
```

Después:

```bash
sudo journalctl -u monolith
```

Para seguir los logs en tiempo real:

```bash
sudo journalctl -u monolith -f
```

---

# 19. Reiniciar la aplicación

Dentro de Ubuntu:

```bash
sudo systemctl restart monolith
```

Verificar:

```bash
sudo systemctl status monolith
```

---

# 20. Detener la aplicación

```bash
sudo systemctl stop monolith
```

Volver a iniciarla:

```bash
sudo systemctl start monolith
```

---

# 21. Ejecutar Ansible nuevamente

Si modificamos el `site.yml` o queremos volver a ejecutar la configuración:

Desde el Mac:

```bash
vagrant provision
```

Vagrant volverá a ejecutar Ansible sobre la VM existente.

No es necesario destruir la VM.

---

# 22. Detener la máquina virtual

Desde el Mac:

```bash
vagrant halt
```

Esto apaga la VM.

Los archivos y la configuración de la VM permanecen.

Para volver a iniciarla:

```bash
vagrant up
```

---

# 23. Destruir la máquina virtual

Si queremos comenzar desde cero:

```bash
vagrant destroy
```

Vagrant pedirá confirmación.

Después:

```bash
vagrant up
```

volverá a crear la VM y Ansible volverá a configurarla desde cero.

---

# 24. Diferencia entre `halt` y `destroy`

### `vagrant halt`

```text
VM
 ↓
apagada
```

La VM sigue existiendo.

### `vagrant destroy`

```text
VM
 ↓
eliminada
```

La próxima vez que ejecutemos:

```bash
vagrant up
```

se creará nuevamente.

---

# 25. Comandos principales

### Crear y configurar

```bash
vagrant up
```

### Ver estado

```bash
vagrant status
```

### Entrar a Ubuntu

```bash
vagrant ssh
```

### Volver a ejecutar Ansible

```bash
vagrant provision
```

### Apagar

```bash
vagrant halt
```

### Eliminar VM

```bash
vagrant destroy
```

---

# 26. Resumen de arquitectura

La arquitectura completa es:

```text
┌───────────────────────────────────────────────┐
│                    macOS                      │
│                                               │
│  Vagrant        VirtualBox        Git         │
│     │               │                           │
│     └───────────────┘                           │
│                     │                           │
│              localhost:8000                    │
└─────────────────────┼─────────────────────────┘
                      │
                      │ Port Forwarding
                      ▼
┌───────────────────────────────────────────────┐
│                  Ubuntu VM                    │
│                                               │
│                   Ansible                     │
│                     │                         │
│                     ▼                         │
│              systemd                         │
│                     │                         │
│                     ▼                         │
│             ┌──────────────┐                  │
│             │    FastAPI   │                  │
│             │    :8000     │                  │
│             │              │                  │
│             │ Users        │                  │
│             │ Orders       │                  │
│             │ Payments     │                  │
│             └──────────────┘                  │
│                                               │
└───────────────────────────────────────────────┘
```

---

# 27. ¿Qué estamos aprendiendo?

Este proyecto permite entender la diferencia entre varias capas:

```text
VirtualBox
    ↓
Máquina virtual

Vagrant
    ↓
Automatización de la máquina virtual

Ansible
    ↓
Configuración del servidor

systemd
    ↓
Administración del proceso

Uvicorn
    ↓
Servidor de la aplicación

FastAPI
    ↓
Aplicación web

Users / Orders / Payments
    ↓
Lógica de negocio
```

La idea fundamental es que **Vagrant y Ansible no determinan si una aplicación es monolítica o de microservicios**.

La arquitectura de la aplicación se encuentra principalmente aquí:

```text
                 Aplicación
                     │
          ┌──────────┴──────────┐
          │                     │
      Monolito             Microservicios
          │                     │
    un proceso          varios procesos
    un puerto            varios puertos
    una app              varias apps
```

Por eso podemos utilizar exactamente las mismas tecnologías de infraestructura para desplegar ambas arquitecturas.
