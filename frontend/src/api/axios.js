import axios from "axios";

// Cria uma instância customizada do Axios
const apiClient = axios.create({
  // Define a URL base para todas as requisições da API
  // baseURL: "http://127.0.0.1:8000/api",
  baseURL: "https://ruthusky.pythonanywhere.com/api",
});

// Adiciona um "interceptor" de requisição.
// Esta função será executada ANTES de cada requisição ser enviada.
apiClient.interceptors.request.use(
  (config) => {
    // 1. Pega o token de acesso do localStorage
    const token = localStorage.getItem("accessToken");

    // 2. Se o token existir, adiciona ao cabeçalho de autorização
    if (token) {
      // O formato é 'Bearer ' porque estamos usando JWT (simplejwt)
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    // 3. Retorna a configuração da requisição para que ela possa continuar
    return config;
  },
  (error) => {
    // Em caso de erro na configuração da requisição, rejeita a promise
    return Promise.reject(error);
  }
);

// Exporta a instância configurada para ser usada em outros lugares do projeto
export default apiClient;
