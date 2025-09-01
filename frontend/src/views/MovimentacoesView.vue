<template>
  <v-container fluid>
    <v-card>
      <v-toolbar color="blue-darken-3">
        <v-toolbar-title>Movimentações de Saída</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="fetchMovimentacoes">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn prepend-icon="mdi-plus" @click="openCreateForm">
          Registrar Saída
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <MovimentacoesList
          :movimentacoes="movimentacoes"
          :loading="loading"
          @edit="openEditForm"
          @delete="confirmDelete"
        />
      </v-card-text>
    </v-card>

    <v-dialog v-model="createDialog" persistent max-width="500px">
      <MovimentacoesForm
        v-if="createDialog"
        @close="createDialog = false"
        @save="saveMovimentacao"
      />
    </v-dialog>

    <v-dialog v-model="editDialog" persistent max-width="400px">
      <v-card>
        <v-card-title>Alterar Status</v-card-title>
        <v-card-text>
          <v-select
            v-model="movimentacaoToEdit.status"
            :items="statusOptions"
            label="Novo Status"
            variant="outlined"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="editDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="updateStatus">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Cancelamento</v-card-title>
        <v-card-text
          >Tem certeza que deseja cancelar esta movimentação?</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">Voltar</v-btn>
          <v-btn color="red-darken-1" @click="deleteMovimentacaoConfirmed"
            >Cancelar Saída</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="errorDialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="text-h5 bg-red-darken-2">
          <v-icon start icon="mdi-alert-circle-outline"></v-icon>
          Erro de Validação
        </v-card-title>
        <v-card-text class="py-4 text-body-1">
          {{ errorMessage }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="elevated"
            @click="errorDialog = false"
          >
            Entendi
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "@/api/axios";
import MovimentacoesList from "@/components/MovimentacoesList.vue";
import MovimentacoesForm from "@/components/MovimentacoesForm.vue";

const movimentacoes = ref([]);
const loading = ref(false);
const createDialog = ref(false);
const editDialog = ref(false);
const deleteDialog = ref(false);
const movimentacaoToEdit = ref({});
const movimentacaoToDelete = ref(null);

// --- Variáveis para o dialog de erro ---
const errorDialog = ref(false);
const errorMessage = ref("");

const statusOptions = [
  "A ENTREGAR",
  "EM ROTA",
  "CONCLUIDO",
  "PENDENTE",
  "CANCELADO",
];

onMounted(() => {
  fetchMovimentacoes();
});

const fetchMovimentacoes = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/movimentacoes/");
    movimentacoes.value = response.data.results;
  } catch (error) {
    console.error("Erro ao buscar movimentações:", error);
  } finally {
    loading.value = false;
  }
};

// --- Funções para gerenciar os dialogs e ações ---
const openCreateForm = () => {
  createDialog.value = true;
};
const openEditForm = (movimentacao) => {
  movimentacaoToEdit.value = { ...movimentacao };
  editDialog.value = true;
};

const saveMovimentacao = async (movimentacao) => {
  try {
    await axios.post("/movimentacoes/", movimentacao);
    createDialog.value = false;
    fetchMovimentacoes();
  } catch (error) {
    // --- LÓGICA DE TRATAMENTO DE ERRO ATUALIZADA ---
    if (error.response && error.response.status === 400) {
      // Se o erro for 400 (Bad Request), provavelmente é nossa validação
      const errorData = error.response.data;
      // O DRF pode enviar erros de várias formas, vamos tratar as mais comuns
      if (typeof errorData === "string") {
        errorMessage.value = errorData;
      } else if (Array.isArray(errorData)) {
        errorMessage.value = errorData.join(" ");
      } else {
        // Pega a mensagem de erro do campo "non_field_errors" ou a primeira que encontrar
        errorMessage.value =
          errorData.non_field_errors?.[0] || Object.values(errorData)[0];
      }
      errorDialog.value = true;
    } else {
      console.error("Erro ao registrar saída:", error);
      // Você pode adicionar um dialog de erro genérico aqui se quiser
    }
  }
};

const updateStatus = async () => {
  try {
    const payload = { status: movimentacaoToEdit.value.status };
    await axios.patch(
      `/movimentacoes/${movimentacaoToEdit.value.id}/`,
      payload
    );
    editDialog.value = false;
    fetchMovimentacoes();
  } catch (error) {
    console.error("Erro ao atualizar status:", error);
  }
};

const confirmDelete = (movimentacao) => {
  movimentacaoToDelete.value = movimentacao;
  deleteDialog.value = true;
};

const deleteMovimentacaoConfirmed = async () => {
  try {
    await axios.delete(`/movimentacoes/${movimentacaoToDelete.value.id}/`);
    deleteDialog.value = false;
    fetchMovimentacoes();
  } catch (error) {
    console.error("Erro ao cancelar movimentação:", error);
    deleteDialog.value = false;
  }
};
</script>
