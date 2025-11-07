document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modalConsulta");
  const btnNovaConsulta = document.getElementById("btnNovaConsulta");
  const btnCancelar = document.getElementById("c_cancelar");
  const btnFechar = document.getElementById("modalClose");
  const form = document.getElementById("formConsulta");

  // Abrir modal
  btnNovaConsulta.addEventListener("click", () => {
    form.reset();
    modal.style.display = "flex";
    document.getElementById("modalTitulo").innerText = "Nova Consulta";
  });

  // Fechar modal
  const fecharModal = () => {
    modal.style.display = "none";
  };
  btnCancelar.addEventListener("click", fecharModal);
  btnFechar.addEventListener("click", fecharModal);

  // Fechar modal ao clicar fora
  window.addEventListener("click", (e) => {
    if (e.target === modal) fecharModal();
  });

  // Enviar formulário (criar nova consulta)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const dataHora = document.getElementById("c_datahora").value;
    const modalidade = document.getElementById("c_modalidade").value;

    // Formatar data
    const dataFormatada = dataHora.replace("T", " ") + ":00";

    const novaConsulta = {
      dataHora: dataFormatada,
      modalidade: modalidade,
    };

    try {
      const resposta = await fetch("http://127.0.0.1:5000/consultas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novaConsulta),
      });

      if (resposta.ok) {
        alert("Consulta cadastrada com sucesso!");
        fecharModal();
        window.location.reload(); // recarrega tabela
      } else {
        const erro = await resposta.json();
        alert("Erro ao salvar consulta: " + (erro.erro || resposta.status));
      }
    } catch (err) {
      console.error("Erro de conexão:", err);
      alert("Erro de conexão com o servidor Flask.");
    }
  });
});
