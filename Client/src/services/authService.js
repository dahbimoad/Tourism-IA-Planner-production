export const login = async (email, password) => {
    // Simuler une requête API
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (email === "test@example.com" && password === "password") {
          resolve({ email, token: "fake-jwt-token" });
        } else {
          reject(new Error("Invalid credentials"));
        }
      }, 1000);
    });
  };
  
  export const isAuthenticated = () => {
    return !!localStorage.getItem("auth");
  };
  