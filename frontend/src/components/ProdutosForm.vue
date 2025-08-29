<template>
  <v-card>
    <v-card-title class="pa-4 bg-blue-darken-3">
      <span class="text-h5">{{ formTitle }}</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" @submit.prevent="save">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="editedProduct.nome"
                label="Nome do Produto"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-switch
                v-model="editedProduct.esta_ativo"
                color="primary"
                label="Produto Ativo"
              ></v-switch>
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
  product: Object,
});

const emits = defineEmits(["close", "save"]);

const form = ref(null);
const editedProduct = ref({ esta_ativo: true }); // Valor padrão para 'esta_ativo'

const rules = {
  required: (v) => !!v || "Campo obrigatório",
};

watch(
  () => props.product,
  (newVal) => {
    editedProduct.value = { ...newVal };
  },
  { immediate: true, deep: true }
);

const formTitle = computed(() => {
  return editedProduct.value.id ? "Editar Produto" : "Novo Produto";
});

const save = async () => {
  const { valid } = await form.value.validate();
  if (valid) {
    emits("save", editedProduct.value);
  }
};

const close = () => {
  emits("close");
};
</script>
