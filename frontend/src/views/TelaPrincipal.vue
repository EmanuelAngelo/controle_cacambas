<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar
      v-if="display.mdAndDown.value"
      title="Gestão de Caçambas"
      color="blue-darken-3"
      density="compact"
    >
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      :permanent="display.mdAndUp.value"
      @click="rail = false"
    >
      <v-list-item prepend-avatar="" :title="userName" nav>
        <template v-slot:append>
          <v-btn
            v-if="display.mdAndUp.value"
            icon="mdi-chevron-left"
            variant="text"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>

      <v-divider></v-divider>

      <div class="d-flex flex-column" style="height: calc(100% - 65px)">
        <v-list density="compact" nav class="flex-grow-1">
          <v-list-item
            prepend-icon="mdi-view-dashboard"
            title="Movimentações"
            value="movimentacoes"
            to="/movimentacoes"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-truck"
            title="Veículos"
            value="veiculos"
            to="/veiculos"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-cube"
            title="Produtos"
            value="produtos"
            to="/produtos"
          ></v-list-item>
        </v-list>

        <div>
          <v-divider></v-divider>
          <v-list density="compact" nav>
            <v-list-item
              prepend-icon="mdi-logout"
              title="Sair"
              value="sair"
              @click="showLogoutDialog = true"
            ></v-list-item>
          </v-list>
        </div>
      </div>
    </v-navigation-drawer>

    <v-main
      class="d-flex align-center justify-center"
      style="min-height: 300px"
    >
      <div class="pa-4" style="width: 100%; height: 100%; overflow-y: auto">
        <router-view />
      </div>
    </v-main>

    <v-dialog v-model="showLogoutDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Confirmar Saída</v-card-title>
        <v-card-text
          >Você tem certeza de que deseja sair do sistema?</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="showLogoutDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn color="red-darken-1" variant="elevated" @click="handleLogout">
            Sair
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script setup>
import { ref, onMounted } from "vue"; // Importe onMounted
import { useRouter } from "vue-router";
import axios from "axios";
import { useDisplay } from "vuetify";

const display = useDisplay();
const drawer = ref(display.mdAndUp.value);
const rail = ref(false);
const router = useRouter();

// --- NOVAS VARIÁVEIS REATIVAS ---
const userName = ref("Usuário"); // Valor padrão
const showLogoutDialog = ref(false); // Controla a visibilidade do dialog

// onMounted é executado quando o componente é montado na tela
onMounted(() => {
  // Busca o nome do usuário salvo no localStorage
  const storedName = localStorage.getItem("userName");
  if (storedName) {
    userName.value = storedName;
  }
});

const handleLogout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("userName"); // Limpa também o nome do usuário
  delete axios.defaults.headers.common["Authorization"];
  showLogoutDialog.value = false; // Fecha o dialog
  router.push("/login");
};
</script>

<style scoped>
.v-layout {
  height: 100vh;
  width: 100vw;
}
</style>
