// === medico.js (versão final) ===
// Front-end da página de Médicos integrado DIRETAMENTE na API (porta 5000)

document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://127.0.0.1:5000";

  const modal = document.getElementById("modalMedico");
  const btnNovo = document.getElementById("btnNovoMedico");
  const btnFechar = document.getElementById("modalClose");
  const btnCancelar = document.getElementById("m_cancelar");
  const form = document.getElementById("formMedico");
  const tbody = document.querySelector("#tbl-medicos tbody");
  const tituloModal = document.getElementById("modalTitulo");

  let modoEdicao = false;
  let medicoEditando = null;

  // ---- Abertura/fechamento do modal ----
  function abrirModal() {
    if (!modal) return;
    modal.classList.add("show"); // compatível com CSS atual
    modal.setAttribute("aria-hidden", "false");
  }

  function fecharModal() {
    if (!modal) return;
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
  }

  if (btnNovo) {
    btnNovo.addEventListener("click", () => {
      modoEdicao = false;
      medicoEditando = null;
      tituloModal.textContent = "Novo Médico";
      form.reset();
      abrirModal();
    });
  }

  [btnFechar, btnCancelar].forEach((btn) => {
    if (btn) btn.addEventListener("click", fecharModal);
  });

  // ---- Renderização das linhas ----
  function renderLinhas(medicos) {
    tbody.innerHTML = "";
    if (!medicos || medicos.length === 0) {
      tbody.innerHTML =
        `<tr><td colspan="7" class="empty-message">Nenhum médico cadastrado.</td></tr>`;
      return;
    }

    for (const m of medicos) {
      const tr = document.createElement("tr");
      tr.dataset.id = m.id;
      tr.dataset.nome = m.nome || "";
      tr.dataset.crm = m.crm || "";
      tr.dataset.especialidade = m.especialidade || "";
      tr.dataset.telefone = m.telefone || "";
      tr.dataset.email = m.email || "";

      tr.innerHTML = `
        <td>${m.id ?? ""}</td>
        <td>${m.nome ?? ""}</td>
        <td>${m.crm ?? ""}</td>
        <td>${m.especialidade ?? ""}</td>
        <td>${m.telefone ?? ""}</td>
        <td>${m.email ?? ""}</td>
        <td>
          <button class="btn btn-sm btnEditar" title="Editar">✎</button>
          <button class="btn btn-sm btnExcluir" title="Excluir" data-id="${m.id}">🗑</button>
        </td>
      `;
      tbody.appendChild(tr);
    }

    configurarBotoes();
  }

  // ---- Carregar lista da API ----
  async function carregarMedicos() {
    try {
      const resp = await fetch(`${API_BASE}/medicos`, { method: "GET" });
      if (!resp.ok) throw new Error(`Falha ao buscar médicos (${resp.status})`);
      const dados = await resp.json();
      renderLinhas(dados);
    } catch (e) {
      console.error("Erro ao carregar médicos:", e);
      tbody.innerHTML =
        `<tr><td colspan="7" class="empty-message">Erro ao carregar médicos.</td></tr>`;
    }
  }

  // ---- Criar/Editar médico ----
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      nome: document.getElementById("m_nome").value.trim(),
      crm: document.getElementById("m_crm").value.trim().toUpperCase(),
      especialidade: document.getElementById("m_espec").value.trim(),
      telefone: document.getElementById("m_tel").value.trim(),
      email: document.getElementById("m_email").value.trim(),
    };

    if (!/^CRM-\d{5}$/.test(payload.crm)) {
      mostrarToast("CRM deve seguir o formato CRM-12345.", "error");
      return;
    }

    try {
      let url = `${API_BASE}/medicos`;
      let method = "POST";

      if (modoEdicao && medicoEditando) {
        url = `${API_BASE}/medicos/${medicoEditando}`;
        method = "PUT";
      }

      const resp = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.erro || `Falha (${resp.status})`);
      }

      fecharModal();
      mostrarToast(
        modoEdicao
          ? "Médico atualizado com sucesso!"
          : "Médico adicionado com sucesso!",
        "success"
      );
      await carregarMedicos();
    } catch (err) {
      console.error(err);
      mostrarToast(`Erro ao salvar médico: ${err.message}`, "error");
    }
  });

  // ---- Botões de ação ----
  function configurarBotoes() {
    document.querySelectorAll(".btnEditar").forEach((btn) => {
      btn.addEventListener("click", () => {
        const tr = btn.closest("tr");
        medicoEditando = tr.dataset.id;
        modoEdicao = true;

        document.getElementById("m_nome").value = tr.dataset.nome || "";
        document.getElementById("m_crm").value = tr.dataset.crm || "";
        document.getElementById("m_espec").value = tr.dataset.especialidade || "";
        document.getElementById("m_tel").value = tr.dataset.telefone || "";
        document.getElementById("m_email").value = tr.dataset.email || "";

        tituloModal.textContent = "Editar Médico";
        abrirModal();
      });
    });

    document.querySelectorAll(".btnExcluir").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        if (!confirm("Deseja realmente excluir este médico?")) return;

        try {
          const resp = await fetch(`${API_BASE}/medicos/${id}`, { method: "DELETE" });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            throw new Error(err.erro || `Falha (${resp.status})`);
          }
          mostrarToast("Médico excluído com sucesso!", "success");
          await carregarMedicos();
        } catch (err) {
          console.error(err);
          mostrarToast(`Erro ao excluir médico: ${err.message}`, "error");
        }
      });
    });
  }

  // ---- Toast simples ----
  function mostrarToast(msg, tipo = "info") {
    const toast = document.createElement("div");
    toast.className = `toast ${tipo}`;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2800);
  }

  // ---- Inicialização ----
  carregarMedicos();
});
