<template>
  <v-data-table
    :headers="headers"
    :items="users"
    :loading="loading"
    class="elevation-1"
    density="compact"
  >
    <template v-slot:loading>
      <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
    </template>

    <template v-slot:item.is_staff="{ value }">
      <v-chip :color="value ? 'primary' : 'grey'" dark small>
        {{ value ? "Admin" : "Operador" }}
      </v-chip>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="$emit('edit', item)"
        >mdi-pencil</v-icon
      >
      <v-icon size="small" @click="$emit('delete', item)">mdi-delete</v-icon>
    </template>
  </v-data-table>
</template>

<script setup>
defineProps({
  users: Array,
  loading: Boolean,
});
defineEmits(["edit", "delete"]);

const headers = [
  { title: "Usuário (Login)", key: "username" },
  { title: "Nome", key: "first_name" },
  { title: "Sobrenome", key: "last_name" },
  { title: "Email", key: "email" },
  { title: "Tipo", key: "is_staff" },
  { title: "Ações", key: "actions", sortable: false, align: "end" },
];
</script>
