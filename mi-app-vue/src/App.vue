<template>
  <div id="app">
    <h1>Aplicación Vue</h1>

    <div class="buttons-container">
      <button @click="toggleSection('reservas')" class="cargar-btn">Reservas</button>
      <button @click="toggleSection('usuarios')" class="cargar-btn">Usuarios</button>
      <button @click="toggleSection('destinos')" class="cargar-btn">Destinos</button>
      <button @click="toggleSection('comentarios')" class="cargar-btn">Comentarios</button>
      <button @click="toggleSection('transportes')" class="cargar-btn">Transportes</button>
      <button @click="toggleSection('extras')" class="cargar-btn">Extras</button>
    </div>

    <div v-if="!currentSection" class="welcome-container">
      <h2>Bienvenido a la Aplicación de Gestión de Viajes</h2>
      <p>Seleccione una categoría para visualizar la información.</p>
    </div>

    <div v-if="currentSection === 'reservas'" class="data-container">
      <h2>Reservas</h2>
      <div v-for="(reserva, index) in reservas" :key="index" class="data-card">
        <p><strong>Código:</strong> {{ reserva.codigo_reserva }}</p>
        <p><strong>Salida:</strong> {{ reserva.fecha_salida }}</p>
        <p><strong>Llegada:</strong> {{ reserva.fecha_llegada }}</p>
        <p><strong>Personas:</strong> {{ reserva.numero_personas }}</p>
        <p><strong>Precio:</strong> {{ reserva.precio }}€</p>
      </div>
    </div>

    <div v-if="currentSection === 'usuarios'" class="data-container">
      <h2>Usuarios</h2>
      <div v-for="(usuario, index) in usuarios" :key="index" class="data-card">
        <p><strong>Nombre:</strong> {{ usuario.nombre }}</p>
        <p><strong>Email:</strong> {{ usuario.email }}</p>
        <p><strong>Edad:</strong> {{ usuario.edad }}</p>
        <p><strong>Teléfono:</strong> {{ usuario.telefono }}</p>
        <p><strong>Registro:</strong> {{ usuario.fecha_registro }}</p>
      </div>
    </div>

    <div v-if="currentSection === 'destinos'" class="data-container">
      <h2>Destinos</h2>
      <div v-for="(destino, index) in destinos" :key="index" class="data-card">
        <p><strong>Nombre:</strong> {{ destino.nombre }}</p>
        <p><strong>País:</strong> {{ destino.pais }}</p>
        <p><strong>Descripción:</strong> {{ destino.descripcion }}</p>
      </div>
    </div>

    <div v-if="currentSection === 'comentarios'" class="data-container">
      <h2>Comentarios</h2>
      <div v-for="(comentario, index) in comentarios" :key="index" class="data-card">
        <p><strong>Usuario:</strong> {{ comentario.usuario }}</p>
        <p><strong>Texto:</strong> {{ comentario.texto }}</p>
        <p><strong>Calificación:</strong> {{ comentario.calificacion }}/5</p>
      </div>
    </div>

    <div v-if="currentSection === 'transportes'" class="data-container">
      <h2>Transportes</h2>
      <div v-for="(transporte, index) in transportes" :key="index" class="data-card">
        <p><strong>Tipo:</strong> {{ transporte.tipo }}</p>
        <p><strong>Empresa:</strong> {{ transporte.empresa }}</p>
        <p><strong>Precio:</strong> {{ transporte.precio }}€</p>
      </div>
    </div>

    <div v-if="currentSection === 'extras'" class="data-container">
      <h2>Extras</h2>
      <div v-for="(extra, index) in extras" :key="index" class="data-card">
        <p><strong>Nombre:</strong> {{ extra.nombre }}</p>
        <p><strong>Descripción:</strong> {{ extra.descripcion }}</p>
        <p><strong>Precio:</strong> {{ extra.precio }}€</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      reservas: [],
      usuarios: [],
      destinos: [],
      comentarios: [],
      transportes: [],
      extras: [],
      currentSection: null
    };
  },
  methods: {
    fetchData(endpoint, target) {
      const token = '1xxfXixpxqxAiiYPpHYtGt1FRGsZ0L';

      axios.get(`http://0.0.0.0:8000/api/v1/${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      .then(response => {
        this[target] = response.data;
      })
      .catch(error => {
        console.error(`Error al cargar ${endpoint}:`, error);
      });
    },
    toggleSection(section) {
      if (this.currentSection === section) {
        this.currentSection = null; // Si ya está visible, ocúltala
      } else {
        this.currentSection = section;
        if (this[section].length === 0) {
          this.fetchData(section, section);
        }
      }
    }
  }
};
</script>

<style scoped>
/* Estilos generales */
#app {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 20px;
  background: #f4f4f9;
  height: 100vh;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

/* Botones */
.buttons-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.cargar-btn {
  padding: 12px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.cargar-btn:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

/* Contenedor de bienvenida */
.welcome-container {
  margin: 20px auto;
  max-width: 800px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.welcome-container h2 {
  color: #444;
}

.welcome-container p {
  color: #666;
  font-size: 16px;
}

/* Contenedor de datos */
.data-container {
  margin: 20px auto;
  max-width: 900px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease-in-out;
}

h2 {
  text-align: left;
  color: #444;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
  margin-bottom: 15px;
}

/* Estilos de las tarjetas */
.data-card {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.data-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

/* Animación de aparición */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
