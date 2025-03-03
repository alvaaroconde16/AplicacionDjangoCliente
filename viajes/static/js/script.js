// script.js
console.log("La página se ha cargado correctamente")

// Realizar la solicitud GET automáticamente cuando la página se carga
fetch("http://0.0.0.0:8000/api/v1/reservas", {
    method: "GET",
    headers: {
        "Authorization": "Bearer 1xxfXixpxqxAiiYPpHYtGt1FRGsZ0L",  // Usa tu token aquí
        "Content-Type": "application/json"
    }
})
.then(response => {
    console.log("Respuesta recibida:", response);
    return response.json();  // Convierte la respuesta a JSON
})
.then(data => {
    console.log("Datos recibidos:", data);
})
.catch(error => {
    console.error("Error:", error);
});
