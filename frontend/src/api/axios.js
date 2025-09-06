import axios from "axios";
import router from "@/router"; // Importamos o router para poder redirecionar

// Cria uma instância customizada do Axios
const apiClient = axios.create({
  // baseURL: "http://127.0.0.1:8000/api",
  baseURL: "https://ruthusky.pythonanywhere.com/api", // Sua URL de produção
});

// --- Interceptor de REQUISIÇÃO (adiciona o token antes de enviar) ---
// (Esta parte você já tem)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- NOVO Interceptor de RESPOSTA (lida com erros, como token expirado) ---
apiClient.interceptors.response.use(
  // Se a resposta for bem-sucedida, apenas a retorna
  (response) => response,

  // Se a resposta der erro, executa esta lógica
  async (error) => {
    const originalRequest = error.config;

    // Verifica se o erro é 401 (Não Autorizado) e se ainda não tentamos renovar o token
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Marca para não tentar renovar infinitamente

      try {
        const refreshToken = localStorage.getItem("refreshToken");
        if (!refreshToken) {
          // Se não houver refresh token, desloga o usuário
          localStorage.removeItem("accessToken");
          localStorage.removeItem("userName");
          localStorage.removeItem("isStaff");
          router.push("/login");
          return Promise.reject(error);
        }

        // Faz a requisição para obter um novo access token
        const response = await apiClient.post("/token/refresh/", {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;

        // Salva o novo token e atualiza os cabeçalhos
        localStorage.setItem("accessToken", newAccessToken);
        apiClient.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

        // Tenta fazer a requisição original novamente com o novo token
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Se a renovação falhar (refresh token também expirou), desloga o usuário
        console.error("Refresh token inválido. Deslogando...");
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("userName");
        localStorage.removeItem("isStaff");
        router.push("/login");
        return Promise.reject(refreshError);
      }
    }

    // Para qualquer outro erro, apenas o rejeita
    return Promise.reject(error);
  }
);

export default apiClient;
