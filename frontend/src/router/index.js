import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import TelaPrincipal from "../views/TelaPrincipal.vue";

// --- Importe as novas views que ficarão DENTRO da TelaPrincipal ---
import HomeView from "../views/HomeView.vue"; // Uma tela inicial padrão
import VeiculosView from "../views/VeiculosView.vue"; // A tela de CRUD de veículos
import ProdutosView from "@/views/ProdutosView.vue";
import MovimentacoesView from "@/views/MovimentacoesView.vue";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    // --- Esta rota se torna o "Layout" principal da aplicação ---
    path: "/",
    component: TelaPrincipal,
    meta: { requiresAuth: true }, // A proteção fica na rota pai
    children: [
      {
        // Rota padrão (página inicial) dentro do layout
        // Será exibida quando você acessar a raiz "/"
        path: "",
        name: "Home",
        component: HomeView,
      },
      {
        // Rota para a tela de Veículos
        // Acessível em "/veiculos"
        path: "veiculos",
        name: "Veiculos",
        component: VeiculosView,
      },
      {
        path: "produtos", // <-- Nova rota
        name: "Produtos",
        component: ProdutosView,
      },
      {
        path: "movimentacoes", // <-- Nova rota
        name: "Movimentacoes",
        component: MovimentacoesView,
      },
      //
      // SUAS FUTURAS ROTAS (Produtos, Movimentações, etc.) ENTRARÃO AQUI
      //
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// "Guarda de Navegação" para proteger as rotas
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem("accessToken");
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth && !loggedIn) {
    next("/login");
  }
  // ATENÇÃO: Mudança aqui para redirecionar para a rota raiz "/"
  else if (to.path === "/login" && loggedIn) {
    next("/");
  } else {
    next();
  }
});

export default router;
