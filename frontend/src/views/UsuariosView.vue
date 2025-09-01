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

const defaultUser = {
  username: "",
  first_name: "",
  last_name: "",
  email: "",
  is_staff: false,
};

onMounted(() => {
  fetchUsers();
});

const fetchUsers = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/usuarios/");
    users.value = response.data.results;
  } catch (error) {
    console.error("Erro ao buscar usuários:", error);
  } finally {
    loading.value = false;
  }
};

const openForm = (user = null) => {
  editedUser.value = user ? { ...user } : { ...defaultUser };
  dialog.value = true;
};

const saveUser = async (user) => {
  try {
    if (user.id) {
      await axios.patch(`/usuarios/${user.id}/`, user); // PATCH é melhor para atualizações parciais
    } else {
      await axios.post("/usuarios/", user);
    }
    dialog.value = false;
    fetchUsers();
  } catch (error) {
    console.error("Erro ao salvar usuário:", error);
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
