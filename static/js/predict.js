const API_URL = "https://python-sprint-privado-4.onrender.com/predict";
const form = document.querySelector(".form-predict");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // Converte strings numéricas para números
  Object.keys(data).forEach((key) => {
    data[key] = isNaN(data[key]) ? data[key] : Number(data[key]);
  });

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);

    const result = await res.json();

    // Esperando algo tipo { "probabilidade": 0.8453 }
    const prob = result.probabilidade.toFixed(2);
    const interpret =
      prob >= 75
        ? "Alta chance de comparecimento ✅"
        : prob >= 50
        ? "Média chance de comparecimento ⚠️"
        : "Baixa chance de comparecimento ❌";

    // Redireciona pro resultado formatado
    window.location.href = `/predict/result?prob=${prob}&interpret=${encodeURIComponent(
      interpret
    )}`;
  } catch (err) {
    console.error("Erro ao calcular previsão:", err);
    alert("Erro ao calcular previsão. Verifique os dados e tente novamente.");
  }
});
