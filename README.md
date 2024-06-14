## SmartEnergy

Este proyecto utiliza una ESP32 para la recolección y envío de datos de consumo energético a través de MQTT. Proporciona una interfaz web para monitorear los datos en tiempo real y analizar tendencias de consumo.

### Características

- **Recolección de Datos:** Utiliza ESP32 para capturar datos de consumo energético.
- **Comunicación:** Envía datos a través del protocolo MQTT para su análisis.
- **Interfaz Web:** Permite visualizar datos en tiempo real y generar reportes.
- **Seguridad:** Implementa autenticación de usuarios y permisos de acceso.

### Tecnologías Utilizadas

- Python
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- Flask-Login
- MQTT
- ESP32

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Lorenzpulgar/SmartEnergy.git
   cd SmartEnergy
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en un archivo `.env` con tus credenciales de base de datos y configuraciones específicas.

4. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

### Uso

1. Accede a la interfaz web desde tu navegador: `http://localhost:5000`
2. Inicia sesión con tus credenciales.
3. Visualiza los datos en tiempo real, accede al dashboard y genera reportes.

### Contribución

Este proyecto está abierto a contribuciones y mejoras. Si deseas colaborar, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y confirma (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

### Licencia

Distribuido bajo la licencia MIT. Consulta `LICENSE` para más información.

### Contacto

Lorenz Pulgar - https://www.linkedin.com/in/lorenzpulgar/
