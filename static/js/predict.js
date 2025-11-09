document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-predict");
  const resultContainer = document.createElement("div");
  resultContainer.id = "predict-result";
  resultContainer.style.marginTop = "20px";
  resultContainer.style.textAlign = "center";
  resultContainer.style.fontSize = "1.2rem";
  form.appendChild(resultContainer);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Função para converter "Sim"/"Não" em 1 e 0
    const toNumber = (value) => (value === "1" || value === "Sim" ? 1 : 0);

    const data = {
      scholarship: parseInt(form.scholarship.value),
      neighbourhood: form.neighbourhood.value.trim(),
      gender: form.gender.value === "M" ? 1 : 0,
      age: parseInt(form.age.value),
      appt_dow: parseInt(form.appt_dow.value),
      handcap: parseInt(form.handcap.value),
      waiting_days: parseInt(form.waiting_days.value),
      hipertension: toNumber(form.hipertension.value),
      sms_received: toNumber(form.sms_received.value),
      alcoholism: toNumber(form.alcoholism.value),
      is_weekend: toNumber(form.is_weekend.value),
      sched_hour: parseInt(form.sched_hour.value),
      diabetes: toNumber(form.diabetes.value),
    };

    console.log("Enviando JSON:", data);

    try {
      const res = await fetch("https://python-sprint-privado-4.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) throw new Error("Erro na resposta da API");

      const result = await res.json();
      console.log("Resposta da API:", result);

      if (result.probabilidade_comparecimento || result.probabilidade) {
        const prob =
          result.probabilidade_comparecimento || `${(result.probabilidade * 100).toFixed(2)}%`;

        resultContainer.innerHTML = `
          <p class="prob-value">Probabilidade de Comparecimento: <strong>${prob}</strong></p>
        `;
      } else {
        resultContainer.innerHTML = `
          <p style="color: red;">Erro ao calcular probabilidade. Tente novamente.</p>
        `;
      }
    } catch (error) {
      console.error("Erro:", error);
      resultContainer.innerHTML = `
        <p style="color: red;">Erro ao conectar com o servidor. Verifique a API.</p>
      `;
    }
  });
});
