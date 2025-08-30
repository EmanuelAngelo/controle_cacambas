<template>
  <v-data-table
    :headers="headers"
    :items="movimentacoes"
    :loading="loading"
    class="elevation-1"
    item-value="id"
    density="compact"
  >
    <template v-slot:loading>
      <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
    </template>

    <template v-slot:item.status="{ value }">
      <v-chip :color="getStatusColor(value)" dark small>
        {{ value }}
      </v-chip>
    </template>

    <template v-slot:item.data_hora_saida="{ item }">
      <span>{{ formatDateTime(item.data_hora_saida) }}</span>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="$emit('edit', item)">
        mdi-pencil
      </v-icon>
      <v-icon size="small" @click="$emit('delete', item)"> mdi-cancel </v-icon>
    </template>
  </v-data-table>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
// --- 1. Importe as funções da date-fns ---
import { format, parseISO } from "date-fns";

defineProps({
  movimentacoes: {
    type: Array,
    default: () => [],
  },
  loading: Boolean,
});

defineEmits(["edit", "delete"]);

const headers = [
  { title: "Veículo", key: "veiculo" },
  { title: "Produto", key: "produto" },
  { title: "Quantidade (m³)", key: "quantidade" },
  { title: "Operador", key: "operador" },
  { title: "Data e Hora", key: "data_hora_saida" },
  { title: "Status", key: "status" },
  { title: "Ações", key: "actions", sortable: false, align: "end" },
];

const getStatusColor = (status) => {
  if (status === "CONCLUIDO") return "green";
  if (status === "CANCELADO") return "red";
  if (status === "EM ROTA") return "yellow";
  return "orange";
};

// --- 2. Crie a função de formatação ---
const formatDateTime = (isoString) => {
  if (!isoString) return "N/A";
  try {
    // 'parseISO' converte a string do backend para um objeto Date do JavaScript
    const date = parseISO(isoString);
    // 'format' converte o objeto Date para o formato desejado
    return format(date, "dd/MM/yyyy HH:mm:ss");
  } catch (error) {
    console.error("Erro ao formatar data:", error);
    return isoString; // Retorna a string original em caso de erro
  }
};
</script>
