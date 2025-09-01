<template>
  <v-container fluid>
    <v-card>
      <v-toolbar color="blue-darken-3">
        <v-toolbar-title>Cadastro de Usuários</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn prepend-icon="mdi-plus" @click="openForm()"
          >Adicionar Usuário</v-btn
        >
      </v-toolbar>

      <v-card-text>
        <UsuariosList
          :users="users"
          :loading="loading"
          @edit="openForm"
          @delete="confirmDelete"
        />
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" persistent max-width="600px">
      <UsuariosForm
        :user="editedUser"
        @close="dialog = false"
        @save="saveUser"
      />
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px"> </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "@/api/axios";
import UsuariosList from "@/components/UsuariosList.vue";
import UsuariosForm from "@/components/UsuariosForm.vue";

const users = ref([]);
const loading = ref(false);
const dialog = ref(false);
const deleteDialog = ref(false);
const editedUser = ref({});
const userToDelete = ref(null);
// Adicione as variáveis para o dialog de erro, caso não as tenha
const errorDialog = ref(false);
const errorMessage = ref("");

// --- PONTO 1: O OBJETO PADRÃO (LIMPO) ---
// Este objeto define o estado inicial do formulário para um novo usuário.
const defaultUser = {
  username: "",
  first_name: "",
  last_name: "",
  email: "",
  password: "", // Importante ter o campo password vazio
  is_staff: false,
};

onMounted(() => {
  fetchUsers();
});

const fetchUsers = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/usuarios/");
    // Se o endpoint for paginado, use .results
    users.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao buscar usuários:", error);
  } finally {
    loading.value = false;
  }
};

// --- PONTO 2: A LÓGICA CORRIGIDA PARA ABRIR O FORMULÁRIO ---
const openForm = (user = null) => {
  if (user) {
    // Modo Edição: Copia os dados do usuário para o formulário
    editedUser.value = { ...user };
  } else {
    // Modo Criação: Copia os dados do objeto padrão (vazio) para o formulário
    editedUser.value = { ...defaultUser };
  }
  dialog.value = true;
};

const saveUser = async (user) => {
  try {
    if (user.id) {
      await axios.patch(`/usuarios/${user.id}/`, user);
    } else {
      await axios.post("/usuarios/", user);
    }
    dialog.value = false;
    fetchUsers();
  } catch (error) {
    console.error("Erro ao salvar usuário:", error);
    // Opcional: mostrar erro de validação do backend
    if (error.response && error.response.status === 400) {
      errorMessage.value = Object.values(error.response.data).join(" ");
      errorDialog.value = true;
    }
  }
};

const confirmDelete = (user) => {
  userToDelete.value = user;
  deleteDialog.value = true;
};

const deleteUserConfirmed = async () => {
  try {
    await axios.delete(`/usuarios/${userToDelete.value.id}/`);
    deleteDialog.value = false;
    fetchUsers();
  } catch (error) {
    console.error("Erro ao excluir usuário:", error);
  }
};
</script>
