document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-predict");

  // Cria a área de resultado logo abaixo do botão
  const resultContainer = document.createElement("div");
  resultContainer.id = "predict-result";
  resultContainer.style.marginTop = "16px";
  resultContainer.style.textAlign = "center";
  resultContainer.style.fontSize = "1.05rem";
  form.appendChild(resultContainer);

  // Funções auxiliares
  const to01 = (v) => (v === "1" || v === "Sim" ? 1 : 0);
  const toInt = (v, d = 0) => {
    const n = parseInt(String(v).trim(), 10);
    return Number.isFinite(n) ? n : d;
  };

  // Mapeamento de bairros para valores numéricos usados pelo modelo
  const neighbourhoodMap = {
    "JARDIM DA PENHA": 1,
    "ITARARÉ": 2,
    "MARUÍPE": 3,
    "CENTRO": 4,
    "SANTA LÚCIA": 5,
    "ILHA DO PRÍNCIPE": 6,
    "JESUS DE NAZARÉ": 7,
    "SANTO ANTÔNIO": 8,
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Converte o bairro selecionado para número
    const selectedNeighbour = form.neighbourhood.value.toUpperCase().trim();
    const neighbourhood = neighbourhoodMap[selectedNeighbour] || 0;

    // Monta o corpo JSON que será enviado
    const data = {
      scholarship: toInt(form.scholarship.value),
      neighbourhood,
      gender: form.gender.value === "M" ? 1 : 0, // F -> 0, M -> 1
      age: toInt(form.age.value),
      appt_dow: toInt(form.appt_dow.value),
      handcap: toInt(form.handcap.value),
      waiting_days: toInt(form.waiting_days.value),
      hipertension: to01(form.hipertension.value),
      sms_received: to01(form.sms_received.value),
      alcoholism: to01(form.alcoholism.value),
      is_weekend: to01(form.is_weekend.value),
      sched_hour: toInt(form.sched_hour.value),
      diabetes: to01(form.diabetes.value),
    };

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const payload = await res.json();

      // Se der erro, mostra mensagem vermelha
      if (!res.ok) {
        console.error("Erro API:", payload);
        resultContainer.innerHTML = `
          <p style="color:#d9534f">
            Erro: ${payload?.erro || "Falha ao calcular previsão."}
          </p>`;
        return;
      }

      // Exibe o resultado formatado
      const prob = payload.probabilidade;
      const probStr = payload.probabilidade_str || `${Number(prob).toFixed(2)}%`;
      const interpret = payload.interpretacao || "";

      resultContainer.innerHTML = `
        <p class="prob-value">
          <strong>Probabilidade de Comparecimento:</strong> 
          <span style="color:#198754">${probStr}</span><br/>
          <span style="color:#198754;font-weight:600">${interpret}</span>
        </p>
      `;
    } catch (err) {
      console.error(err);
      resultContainer.innerHTML = `
        <p style="color:#d9534f">
          Erro ao conectar com o servidor. Verifique a API.
        </p>`;
    }
  });
});
