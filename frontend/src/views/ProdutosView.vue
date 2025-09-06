<template>
  <v-container fluid>
    <v-card>
      <v-toolbar color="blue-darken-3">
        <v-toolbar-title>Cadastro de Produtos</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="fetchProducts">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn prepend-icon="mdi-plus" @click="openForm()">
          Adicionar Produto
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <ProdutosList
          :products="products"
          :loading="loading"
          @edit="openForm"
          @delete="confirmDelete"
        />
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" persistent max-width="500px">
      <ProdutosForm
        :product="editedProduct"
        @close="dialog = false"
        @save="saveProduct"
      />
    </v-dialog>

    <v-dialog v-model="deleteDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Exclusão</v-card-title>
        <v-card-text>Tem certeza que deseja excluir este produto?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">Cancelar</v-btn>
          <v-btn color="red-darken-1" @click="deleteProductConfirmed"
            >Excluir</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="errorDialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="text-h5 bg-red-darken-2">
          <v-icon start icon="mdi-alert-circle-outline"></v-icon>
          Operação Bloqueada
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
    <v-dialog v-model="errorDialog" persistent max-width="500px">
      <v-card>
        <v-card-title class="text-h5 bg-red-darken-2">
          <v-icon start icon="mdi-alert-circle-outline"></v-icon>
          Operação Bloqueada
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
import ProdutosList from "@/components/ProdutosList.vue";
import ProdutosForm from "@/components/ProdutosForm.vue";

const products = ref([]);
const loading = ref(false);
const dialog = ref(false);
const deleteDialog = ref(false);
const editedProduct = ref({});
const productToDelete = ref(null);
const errorDialog = ref(false);
const errorMessage = ref("");

const defaultProduct = {
  nome: "",
  esta_ativo: true,
};

onMounted(() => {
  fetchProducts();
});

const fetchProducts = async () => {
  loading.value = true;
  try {
    const response = await axios.get("/produtos/");
    products.value = response.data.results;
  } catch (error) {
    console.error("Erro ao buscar produtos:", error);
  } finally {
    loading.value = false;
  }
};

const openForm = (product = null) => {
  editedProduct.value = product ? { ...product } : { ...defaultProduct };
  dialog.value = true;
};

const saveProduct = async (product) => {
  try {
    if (product.id) {
      await axios.put(`/produtos/${product.id}/`, product);
    } else {
      await axios.post("/produtos/", product);
    }
    dialog.value = false;
    fetchProducts();
  } catch (error) {
    console.error("Erro ao salvar produto:", error);
  }
};

const confirmDelete = (product) => {
  productToDelete.value = product;
  deleteDialog.value = true;
};

const deleteProductConfirmed = async () => {
  try {
    await axios.delete(`/produtos/${productToDelete.value.id}/`);
    deleteDialog.value = false;
    fetchProducts();
  } catch (error) {
    deleteDialog.value = false;
    if (error.response && error.response.status === 409) {
      // Mensagem de erro específica para produtos
      errorMessage.value =
        "Este produto não pode ser excluído, pois está associado a uma ou mais movimentações.";
      errorDialog.value = true;
    } else {
      errorMessage.value =
        "Ocorreu um erro inesperado ao tentar excluir o produto.";
      errorDialog.value = true;
    }
    console.error("Erro ao excluir produto:", error);
  }
};
</script>
