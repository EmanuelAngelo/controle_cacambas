<template>
  <v-container fluid class="fill-height bg-grey-lighten-4">
    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12 pa-4">
          <v-card-title
            class="text-center text-h5 font-weight-bold text-blue-darken-2"
          >
            Gestão de Caçambas
          </v-card-title>
          <v-card-subtitle class="text-center mb-6">
            Acesse sua conta para continuar
          </v-card-subtitle>

          <v-card-text>
            <v-form @submit.prevent="handleLogin" ref="form">
              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                closable
                class="mb-4"
                density="compact"
              >
                {{ errorMessage }}
              </v-alert>

              <v-text-field
                v-model="username"
                label="Usuário"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                :rules="[rules.required]"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Senha"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                :rules="[rules.required]"
                required
                class="mt-2"
              ></v-text-field>

              <v-btn
                :loading="loading"
                type="submit"
                color="blue-darken-3"
                size="large"
                block
                class="mt-4"
              >
                Entrar
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "@/api/axios.js";

const form = ref(null);
const username = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");
const router = useRouter();

const rules = {
  required: (value) => !!value || "Este campo é obrigatório.",
};

// --- FUNÇÃO DE LOGIN ATUALIZADA ---
// ... (resto do script setup)
const handleLogin = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await axios.post("/token/", {
      // URL agora é relativa
      username: username.value,
      password: password.value,
    });

    if (response.data.access) {
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);

      // --- MUDANÇA 2: Esta linha não é mais necessária! ---
      // O interceptor em 'axios.js' já cuida disso automaticamente
      // axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;

      const userResponse = await axios.get("/me/"); // URL agora é relativa
      localStorage.setItem(
        "userName",
        userResponse.data.first_name || userResponse.data.username
      );
      localStorage.setItem("isStaff", userResponse.data.is_staff);

      router.push("/");
    }
  } catch (error) {
    if (
      error.response &&
      (error.response.status === 400 || error.response.status === 401)
    ) {
      errorMessage.value = "Usuário ou senha inválidos.";
    } else {
      errorMessage.value = "Ocorreu um erro de conexão.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.bg-grey-lighten-4 {
  background: url("https://www.ssab.com/_next/image?url=https%3A%2F%2Fwww.ssab.com%2F%2F-%2Fmedia%2Fimages%2Fhardox%2Fhimb-new%2F1920x1080-bucket-top.jpg%3Fm%3D20210407181724&w=3840&q=75")
    no-repeat center center fixed !important;
  background-size: cover;
}
</style>
