document.addEventListener("DOMContentLoaded", () => {
  const formPrever = document.getElementById("formPrever");
  const resultadoDiv = document.getElementById("resultado");

  if (!formPrever) return; // só executa se estiver na página prever

  formPrever.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(formPrever);
    const dados = Object.fromEntries(formData.entries());

    // Conversão de gênero (H/M → 1/0)
    if (dados.gender) {
      const genero = dados.gender.trim().toUpperCase();
      if (genero === "H") dados.gender = 1;
      else if (genero === "M") dados.gender = 0;
      else {
        resultadoDiv.innerHTML = `<p style="color:red;">⚠️ Valor inválido em "Gênero". Use H (homem) ou M (mulher).</p>`;
        return;
      }
    }

    // Conversão de valores numéricos
    for (let key in dados) {
      const val = dados[key];
      if (!isNaN(val) && val !== "") {
        dados[key] = parseFloat(val);
      }
    }

    // Mostra carregando
    resultadoDiv.innerHTML = `
      <p style="color:#007bff; font-weight:bold;">⏳ Processando previsão...</p>
    `;

    try {
      const resposta = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });

      const resultado = await resposta.json();

      if (resultado.probabilidade_comparecimento) {
        const prob = parseFloat(resultado.probabilidade_comparecimento);
        const cor = prob >= 70 ? "#28a745" : "#dc3545";
        const emoji = prob >= 70 ? "✅" : "⚠️";

        resultadoDiv.innerHTML = `
          <div style="
            background-color:${prob >= 70 ? '#e8f5e9' : '#fdecea'};
            border-left:5px solid ${cor};
            padding:15px;
            border-radius:8px;
            text-align:center;
          ">
            <h5>Resultado da IA:</h5>
            <p style="font-size:18px; font-weight:bold; color:${cor};">
              ${emoji} ${resultado.mensagem}<br>
              Probabilidade: ${prob}%
            </p>
          </div>
        `;
      } else if (resultado.erro) {
        resultadoDiv.innerHTML = `<p style="color:red;">❌ Erro: ${resultado.erro}</p>`;
      } else {
        resultadoDiv.innerHTML = `<p style="color:gray;">Nenhum resultado retornado.</p>`;
      }
    } catch (error) {
      console.error(error);
      resultadoDiv.innerHTML = `<p style="color:red;">❌ Erro ao conectar com o servidor.</p>`;
    }
  });
});
