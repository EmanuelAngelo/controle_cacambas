<template>
  <v-card>
    <v-card-title class="pa-4 bg-blue-darken-3">
      <span class="text-h5">{{ formTitle }}</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" @submit.prevent="save">
        <v-container>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="editedVehicle.placa"
                label="Placa do Veículo"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="editedVehicle.numero_interno"
                label="Número Interno"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="editedVehicle.marca"
                label="Marca"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="editedVehicle.tipo"
                label="Tipo"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="editedVehicle.capacidade"
                label="Capacidade (m³)"
                type="number"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>

    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn color="blue-grey-darken-1" variant="text" @click="close">
        Cancelar
      </v-btn>
      <v-btn color="blue-darken-3" variant="elevated" @click="save">
        Salvar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from "vue";

const props = defineProps({
  vehicle: Object,
});

const emits = defineEmits(["close", "save"]);

const form = ref(null);
const editedVehicle = ref({});

const rules = {
  required: (v) => !!v || "Campo obrigatório",
};

// Observa o 'prop' vehicle. Quando ele muda, atualiza o formulário.
watch(
  () => props.vehicle,
  (newVal) => {
    // O 'spread operator' ({...newVal}) cria uma cópia para evitar alterar o original
    editedVehicle.value = { ...newVal };
  },
  { immediate: true, deep: true }
);

const formTitle = computed(() => {
  return editedVehicle.value.id ? "Editar Veículo" : "Novo Veículo";
});

const save = async () => {
  const { valid } = await form.value.validate();
  if (valid) {
    emits("save", editedVehicle.value);
  }
};

const close = () => {
  emits("close");
};
</script>
