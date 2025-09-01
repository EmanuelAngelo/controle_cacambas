<template>
  <v-card>
    <v-card-title class="pa-4 bg-blue-darken-3">
      <span class="text-h5">{{ formTitle }}</span>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" @submit.prevent="save">
        <v-container>
          <v-row>
            <v-col cols="12"
              ><v-text-field
                v-model="editedUser.username"
                label="Usuário (para login)"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              ></v-text-field
            ></v-col>
            <v-col cols="12" sm="6"
              ><v-text-field
                v-model="editedUser.first_name"
                label="Nome"
                variant="outlined"
                density="compact"
              ></v-text-field
            ></v-col>
            <v-col cols="12" sm="6"
              ><v-text-field
                v-model="editedUser.last_name"
                label="Sobrenome"
                variant="outlined"
                density="compact"
              ></v-text-field
            ></v-col>
            <v-col cols="12"
              ><v-text-field
                v-model="editedUser.email"
                label="Email"
                :rules="[rules.required, rules.email]"
                variant="outlined"
                density="compact"
              ></v-text-field
            ></v-col>
            <v-col cols="12"
              ><v-text-field
                v-model="editedUser.password"
                label="Senha"
                :placeholder="passwordPlaceholder"
                type="password"
                variant="outlined"
                density="compact"
              ></v-text-field
            ></v-col>
            <v-col cols="12"
              ><v-switch
                v-model="editedUser.is_staff"
                color="primary"
                label="Este usuário é Administrador"
              ></v-switch
            ></v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>

    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn text @click="close">Cancelar</v-btn>
      <v-btn color="primary" @click="save">Salvar</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, watch, computed } from "vue";

const props = defineProps({ user: Object });
const emits = defineEmits(["close", "save"]);

const form = ref(null);
const editedUser = ref({});

const rules = {
  required: (v) => !!v || "Campo obrigatório",
  email: (v) => /.+@.+\..+/.test(v) || "E-mail inválido",
};

watch(
  () => props.user,
  (newVal) => {
    editedUser.value = { ...newVal };
  },
  { immediate: true, deep: true }
);

const formTitle = computed(() =>
  editedUser.value.id ? "Editar Usuário" : "Novo Usuário"
);
const passwordPlaceholder = computed(() =>
  editedUser.value.id ? "Deixe em branco para não alterar" : ""
);

const save = async () => {
  const { valid } = await form.value.validate();
  if (valid) {
    // Remove a senha se estiver vazia para não enviar ao backend
    if (!editedUser.value.password) {
      delete editedUser.value.password;
    }
    emits("save", editedUser.value);
  }
};
const close = () => {
  emits("close");
};
</script>
