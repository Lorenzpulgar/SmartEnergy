# SmartEnergy 🌐⚡

Un proyecto que combina tecnología IoT y domótica para revolucionar el monitoreo energético en tiempo real y abrir el camino hacia automatizaciones inteligentes. Con el potencial de integrar Inteligencia Artificial, **SmartEnergy** puede ser el núcleo de un sistema avanzado de domótica para hogares inteligentes.

---

## 🚀 Visión Futurista: IA en Domótica 🏠🤖

Imagina un hogar donde **SmartEnergy** no solo monitorea el consumo energético, sino que también:
- Predice patrones de uso energético y optimiza el consumo con algoritmos de IA. 🧠
- Automatiza dispositivos como luces, electrodomésticos y climatización basándose en datos históricos y condiciones actuales. 🔌
- Integra asistentes virtuales para gestionar el consumo energético de manera eficiente. 🎙️
- Detecta anomalías y emite alertas para evitar desperdicio o posibles fallos. 🚨

---

## 🌟 Características Actuales

### 🔍 **Recolección y Análisis de Datos**
- Utiliza una ESP32 para capturar datos de consumo energético.
- Envía datos a través del protocolo **MQTT** para procesamiento y análisis.

### 🌐 **Interfaz Web**
- Visualiza datos en tiempo real a través de un dashboard interactivo.
- Genera reportes detallados para análisis energético.

### 🔒 **Seguridad**
- Implementa autenticación de usuarios y permisos de acceso.

---

## 🛠️ Tecnologías Utilizadas

- **Python** y **Flask** para el backend.
- **SQLAlchemy** y **Flask-SQLAlchemy** para la gestión de base de datos.
- **Flask-Login** para autenticación.
- **MQTT** para comunicación IoT.
- **ESP32** como dispositivo de recolección.

---

## ⚙️ Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Lorenzpulgar/SmartEnergy.git
   cd SmartEnergy
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en un archivo `.env` con tus credenciales de base de datos.

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

---

## 🌟 Uso

1. Accede a la interfaz web desde tu navegador: `http://localhost:5000`.
2. Inicia sesión con tus credenciales.
3. Visualiza los datos en tiempo real, accede al dashboard y genera reportes.

---

## 🤝 Contribución

Este proyecto está abierto a contribuciones. Si deseas colaborar:
1. Haz un fork del repositorio.
2. Crea una rama:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y confirma:
   ```bash
   git commit -am 'Agrega nueva funcionalidad'
   ```
4. Haz push a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un Pull Request.

---

## 📜 Licencia

Distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---

## 📞 Contacto

Lorenz Pulgar - [LinkedIn](https://www.linkedin.com/in/lorenzpulgar/)

---

**SmartEnergy: Transformando hogares, un watt a la vez. 🌟**
