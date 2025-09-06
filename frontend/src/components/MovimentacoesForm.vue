<template>
  <v-card>
    <v-card-title class="pa-4 bg-blue-darken-3">
      <span class="text-h5">Registrar Nova Saída</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" @submit.prevent="save">
        <v-container>
          <v-row>
            <v-col cols="12" v-if="isStaff">
              <v-autocomplete
                v-model="editedMovimentacao.operador"
                :items="operadores"
                item-title="username"
                item-value="id"
                label="Selecione o Operador (Admin)"
                variant="outlined"
                density="compact"
                :rules="[rules.required]"
              ></v-autocomplete>
            </v-col>

            <v-col cols="12">
              <v-autocomplete
                v-model="editedMovimentacao.veiculo"
                :items="veiculos"
                item-title="placa"
                item-value="id"
                label="Selecione o Veículo"
                variant="outlined"
                density="compact"
                :rules="[rules.required]"
              ></v-autocomplete>
            </v-col>

            <v-col cols="12">
              <v-autocomplete
                v-model="editedMovimentacao.produto"
                :items="produtos"
                item-title="nome"
                item-value="id"
                label="Selecione o Produto"
                variant="outlined"
                density="compact"
                :rules="[rules.required]"
              ></v-autocomplete>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="editedMovimentacao.quantidade"
                label="Quantidade Transportada (m³)"
                type="number"
                variant="outlined"
                density="compact"
                :rules="[rules.required]"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="editedMovimentacao.valor_entrega"
                label="Valor da Entrega (R$)"
                type="number"
                variant="outlined"
                density="compact"
                :rules="[rules.required]"
              ></v-text-field>
            </v-col>
            <v-divider class="my-4">Destinatário</v-divider>

            <v-col cols="12">
              <v-text-field
                v-model="editedMovimentacao.nome_destinatario"
                label="Nome do Destinatário (Opcional)"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="editedMovimentacao.telefone_destinatario"
                label="Telefone do Destinatário (Opcional)"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="editedMovimentacao.endereco_entrega"
                label="Endereço de Entrega (Opcional)"
                variant="outlined"
                density="compact"
                rows="3"
              ></v-textarea>
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
        Registrar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script setup>
import { ref, onMounted, computed, defineEmits } from "vue";
import axios from "@/api/axios";

const emits = defineEmits(["close", "save"]);

const form = ref(null);
const editedMovimentacao = ref({});

const veiculos = ref([]);
const produtos = ref([]);
const valor_entrega = ref([]);
const operadores = ref([]);

const isStaff = computed(() => localStorage.getItem("isStaff") === "true");

const rules = {
  required: (v) => !!v || "Campo obrigatório",
};

onMounted(async () => {
  try {
    // Prepara a lista de requisições a serem feitas
    const requests = [axios.get("/veiculos/"), axios.get("/produtos/")];

    // Se o usuário for um admin, adiciona a busca de usuários à lista
    if (isStaff.value) {
      requests.push(axios.get("/usuarios/"));
    }

    // Executa todas as requisições em paralelo
    const responses = await Promise.all(requests);

    // Atribui os resultados às variáveis reativas
    veiculos.value = responses[0].data.results;
    produtos.value = responses[1].data.results;

    // Se for admin, a terceira resposta será a dos usuários
    if (isStaff.value && responses[2]) {
      // --- MUDANÇA AQUI: Adicionar .results ---
      // A lista de usuários também vem paginada do backend
      operadores.value = responses[2].data.results;
    }
  } catch (error) {
    console.error("Erro ao carregar dados para o formulário:", error);
    if (error.response?.status === 403) {
      console.error(
        "Atenção: O usuário logado não tem permissão para listar operadores."
      );
    }
  }
});

const save = async () => {
  const { valid } = await form.value.validate();
  if (valid) {
    emits("save", editedMovimentacao.value);
  }
};

const close = () => {
  emits("close");
};
</script>
