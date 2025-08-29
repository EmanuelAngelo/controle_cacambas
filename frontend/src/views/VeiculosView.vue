<template>
  <v-container fluid>
    <v-card>
      <v-toolbar color="blue-darken-3">
        <v-toolbar-title>Cadastro de Veículos</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="fetchVehicles">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn prepend-icon="mdi-plus" @click="openForm()">
          Adicionar Veículo
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <VeiculosList
          :vehicles="vehicles"
          :loading="loading"
          @edit="openForm"
          @delete="confirmDelete"
        />
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" persistent max-width="600px">
      <VeiculosForm
        :vehicle="editedVehicle"
        @close="dialog = false"
        @save="saveVehicle"
      />
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
        <v-card-text>Tem certeza que deseja excluir este veículo?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="red-darken-1" @click="deleteVehicleConfirmed"
            >Excluir</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import VeiculosList from "@/components/VeiculosList.vue";
import VeiculosForm from "@/components/VeiculosForm.vue";

const vehicles = ref([]);
const loading = ref(false);
const dialog = ref(false);
const deleteDialog = ref(false);
const editedVehicle = ref({});
const vehicleToDelete = ref(null);

const defaultVehicle = {
  placa: "",
  numero_interno: "",
  marca: "",
  tipo: "",
  capacidade: 0,
};

onMounted(() => {
  fetchVehicles();
});

const fetchVehicles = async () => {
  loading.value = true;
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/veiculos/");
    vehicles.value = response.data.results;
  } catch (error) {
    console.error("Erro ao buscar veículos:", error);
  } finally {
    loading.value = false;
  }
};

const openForm = (vehicle = null) => {
  editedVehicle.value = vehicle ? { ...vehicle } : { ...defaultVehicle };
  dialog.value = true;
};

const saveVehicle = async (vehicle) => {
  try {
    if (vehicle.id) {
      // Atualizar (PUT)
      await axios.put(
        `http://127.0.0.1:8000/api/veiculos/${vehicle.id}/`,
        vehicle
      );
    } else {
      // Criar (POST)
      await axios.post("http://127.0.0.1:8000/api/veiculos/", vehicle);
    }
    dialog.value = false;
    fetchVehicles(); // Atualiza a lista
  } catch (error) {
    console.error("Erro ao salvar veículo:", error);
  }
};

const confirmDelete = (vehicle) => {
  vehicleToDelete.value = vehicle;
  deleteDialog.value = true;
};

const deleteVehicleConfirmed = async () => {
  try {
    await axios.delete(
      `http://127.0.0.1:8000/api/veiculos/${vehicleToDelete.value.id}/`
    );
    deleteDialog.value = false;
    fetchVehicles(); // Atualiza a lista
  } catch (error) {
    console.error("Erro ao excluir veículo:", error);
  }
};
</script>
