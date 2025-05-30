const config = {
    // En desarrollo usamos localhost, en producción usaremos la URL de la VM
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
    // Otros valores de configuración pueden ir aquí
};

export default config; 