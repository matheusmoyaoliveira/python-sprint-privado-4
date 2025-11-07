// TOAST global (usado em várias páginas)
export function toast(msg, type="ok"){
  const box = document.createElement("div");
  box.className = `toast ${type}`;
  box.textContent = msg;
  document.body.appendChild(box);
  setTimeout(()=>box.classList.add("show"), 10);
  setTimeout(()=>box.classList.remove("show"), 3000);
  setTimeout(()=>box.remove(), 3400);
}

// --- PREVER ---
document.querySelector("#formPrever")?.addEventListener("submit", async (e)=>{
  e.preventDefault();
  const payload = {
    idade: document.querySelector("#p_idade").value,
    genero: document.querySelector("#p_genero").value,
    possui_bolsa: document.querySelector("#p_bolsa").value,
    hipertenso: document.querySelector("#p_hipertenso").value,
    diabetico: document.querySelector("#p_diabetico").value,
    alcoolatra: document.querySelector("#p_alcoolatra").value,
    deficiencia: document.querySelector("#p_deficiencia").value,
    recebeu_sms: document.querySelector("#p_sms").value,
    dias_espera: document.querySelector("#p_dias").value,
    dia_semana: document.querySelector("#p_dia_semana").value,
    hora_consulta: document.querySelector("#p_hora").value,
    final_semana: document.querySelector("#p_fds").value
  };

  const res = await fetch("/api/prever", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });
  const json = await res.json();

  const box = document.querySelector("#preverResposta");
  if (json.ok){
    box.innerHTML = `
      <div class="alert ok">
        <strong>Resultado:</strong> ${json.data.classe}<br>
        <small>Probabilidade: ${json.data.probabilidade_comparecimento}</small>
      </div>`;
  } else {
    box.innerHTML = `<div class="alert err">Erro: ${json.error}</div>`;
  }
});
