<template>
  <v-data-table
    :headers="headers"
    :items="vehicles"
    :loading="loading"
    class="elevation-1"
    item-value="id"
    density="compact"
  >
    <template v-slot:loading>
      <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="$emit('edit', item)">
        mdi-pencil
      </v-icon>
      <v-icon size="small" @click="$emit('delete', item)"> mdi-delete </v-icon>
    </template>
  </v-data-table>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps({
  vehicles: {
    type: Array,
    default: () => [],
  },
  loading: Boolean,
});

defineEmits(["edit", "delete"]);

const headers = [
  { title: "Placa", key: "placa" },
  { title: "Número Interno", key: "numero_interno" },
  { title: "Marca", key: "marca" },
  { title: "Tipo", key: "tipo" },
  { title: "Capacidade (m³)", key: "capacidade" },
  { title: "Ações", key: "actions", sortable: false, align: "end" },
];
</script>
