// ================= MÉDICOS =================
const API_URL = "https://python-sprint-privado-4.onrender.com/api/medicos";

const form = document.getElementById("formMedico");
const container = document.getElementById("listaMedicos");

// ============ FORMATAÇÃO CRM ============
function formatarCRM(crm) {
  crm = crm.replace(/\D/g, ""); // remove tudo que não for número
  return `CRM-${crm}`; // padrão fixo
}

// ================== CARREGAR MÉDICOS (GET) ==================
async function carregarMedicos() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Erro ${res.status}`);

    const medicos = await res.json();
    container.innerHTML = "";

    if (medicos.length === 0) {
      container.innerHTML = `<p style="text-align:center;">Nenhum médico cadastrado.</p>`;
      return;
    }

    medicos.forEach((m) => {
      const card = document.createElement("div");
      card.classList.add("card");

      card.innerHTML = `
        <div class="card-header">${m.nome}</div>
        <div class="card-body">
          <p><strong>CRM:</strong> ${m.crm}</p>
          <p><strong>Especialidade:</strong> ${m.especialidade}</p>
        </div>
        <div class="card-actions">
          <button class="btn-excluir" onclick="excluirMedico(${m.id})">Excluir</button>
          <button class="btn-editar" onclick="editarMedico(${m.id})">Editar</button>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (error) {
    console.error("❌ Erro ao carregar médicos:", error);
    container.innerHTML = `<p style="color:red; text-align:center;">Erro ao carregar médicos.</p>`;
  }
}

// ================== ADICIONAR MÉDICO (POST) ==================
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const crm = document.getElementById("crm").value.trim();
  const especialidade = document.getElementById("especialidade").value.trim();

  if (!nome || !crm || !especialidade) {
    alert("Por favor, preencha todos os campos!");
    return;
  }

  const novoMedico = {
    nome,
    crm: formatarCRM(crm),
    especialidade
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(novoMedico),
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("✅ Médico adicionado com sucesso!");
    form.reset();
    carregarMedicos();
  } catch (error) {
    console.error("❌ Erro ao adicionar médico:", error);
    alert("Erro ao adicionar médico.");
  }
});

// ================== EDITAR MÉDICO (PUT) ==================
async function editarMedico(id) {
  const novoNome = prompt("Digite o novo nome:");
  const novoCrm = prompt("Digite o novo CRM (apenas números):");
  const novaEsp = prompt("Digite a nova especialidade:");

  if (!novoNome || !novoCrm || !novaEsp) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  const payload = {
    nome: novoNome.trim(),
    crm: formatarCRM(novoCrm),
    especialidade: novaEsp.trim(),
  };

  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("✅ Médico atualizado com sucesso!");
    carregarMedicos();
  } catch (err) {
    console.error("❌ Erro ao editar médico:", err);
    alert("Erro ao editar médico.");
  }
}

// ================== EXCLUIR MÉDICO (DELETE) ==================
async function excluirMedico(id) {
  if (!confirm("Tem certeza que deseja excluir este médico?")) return;

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("🗑️ Médico excluído com sucesso!");
    carregarMedicos();
  } catch (err) {
    console.error("❌ Erro ao excluir médico:", err);
    alert("Erro ao excluir médico.");
  }
}

// ================== INICIALIZA ==================
carregarMedicos();
