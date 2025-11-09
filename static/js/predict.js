document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-predict");

  // área de resultado abaixo do botão
  const resultContainer = document.createElement("div");
  resultContainer.id = "predict-result";
  resultContainer.style.marginTop = "16px";
  resultContainer.style.textAlign = "center";
  resultContainer.style.fontSize = "1.05rem";
  form.appendChild(resultContainer);

  const to01 = (v) => (v === "1" || v === "Sim" ? 1 : 0);
  const toInt = (v, d = 0) => {
    const n = parseInt(String(v).trim(), 10);
    return Number.isFinite(n) ? n : d;
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Se o input do bairro for texto, vira 0 (ou troca por um código)
    const rawNeighbour = form.neighbourhood.value;
    const neighbourhood = toInt(rawNeighbour, 0);

    const data = {
      scholarship: toInt(form.scholarship.value),
      neighbourhood,
      gender: form.gender.value === "M" ? 1 : 0, // F->0, M->1
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

      if (!res.ok) {
        console.error("Erro API:", payload);
        resultContainer.innerHTML = `<p style="color:#d9534f">Erro: ${payload?.erro || "Falha ao calcular previsão."}</p>`;
        return;
      }

      const prob = payload.probabilidade; // número
      const probStr = payload.probabilidade_str || `${Number(prob).toFixed(2)}%`;

      resultContainer.innerHTML = `
        <p class="prob-value">
          <strong>Probabilidade de Comparecimento:</strong> ${probStr}<br/>
          <span style="opacity:.9">${payload.interpretacao || ""}</span>
        </p>
      `;
    } catch (err) {
      console.error(err);
      resultContainer.innerHTML = `<p style="color:#d9534f">Erro ao conectar com o servidor. Verifique a API.</p>`;
    }
  });
});
