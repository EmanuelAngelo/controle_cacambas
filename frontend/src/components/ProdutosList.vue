<template>
  <v-data-table
    :headers="headers"
    :items="products"
    :loading="loading"
    class="elevation-1"
    item-value="id"
    density="compact"
  >
    <template v-slot:loading>
      <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
    </template>

    <template v-slot:item.esta_ativo="{ value }">
      <v-chip :color="value ? 'green' : 'red'" dark small>
        {{ value ? "Ativo" : "Inativo" }}
      </v-chip>
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
  products: {
    type: Array,
    default: () => [],
  },
  loading: Boolean,
});

defineEmits(["edit", "delete"]);

const headers = [
  { title: "Nome do Produto", key: "nome" },
  { title: "Status", key: "esta_ativo" },
  { title: "Ações", key: "actions", sortable: false, align: "end" },
];
</script>
