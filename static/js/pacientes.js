// URL da API pública hospedada no Render
const API_URL = "https://python-sprint-privado-4.onrender.com/api/pacientes";

// Elementos do DOM
const form = document.getElementById("formPaciente");
const container = document.getElementById("pacientesContainer");

// =============== LISTAR PACIENTES (GET) ===============
async function carregarPacientes() {
  try {
    const res = await fetch(API_URL);
    console.log("Status:", res.status, "URL:", API_URL);
    if (!res.ok) throw new Error("Erro ao listar pacientes");

    const pacientes = await res.json();
    container.innerHTML = "";

    pacientes.forEach(p => {
      const card = document.createElement("div");
      card.classList.add("card-paciente");
      card.innerHTML = `
        <div class="card-header">
          <h3>${p.nome}</h3>
          <p class="small">ID #${p.id}</p>
        </div>
        <div class="card-body">
          <p><b>Idade:</b> ${p.idade}</p>
          <p><b>CPF:</b> ${p.cpf}</p>
          <p><b>Telefone:</b> ${p.telefone}</p>
        </div>
        <div class="card-footer">
          <button class="btn btn-delete" onclick="excluirPaciente(${p.id})">Excluir</button>
          <button class="btn-editar" onclick="editarPaciente(${p.id})">Editar</button>
        </div>
      `;
      container.appendChild(card);
    });

  } catch (error) {
    console.error("❌ Erro ao carregar pacientes:", error);
    container.innerHTML = `<p style="color:red;">Erro ao carregar pacientes.</p>`;
  }
}

// =============== ADICIONAR PACIENTE (POST) ===============
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const novoPaciente = {
    nome: document.getElementById("nome").value,
    idade: document.getElementById("idade").value,
    cpf: document.getElementById("cpf").value,
    telefone: document.getElementById("telefone").value
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(novoPaciente)
    });

    if (!res.ok) throw new Error("Erro ao adicionar paciente");

    form.reset();
    carregarPacientes();
  } catch (error) {
    console.error("❌ Erro ao adicionar paciente:", error);
    alert("Erro ao adicionar paciente!");
  }
});

// =============== EDITAR PACIENTE (PUT) ===============

async function editarPaciente(id) {
  const novoNome = prompt("Digite o novo nome:");
  const novaIdade = prompt("Digite a nova idade:");
  const novoCpf = prompt("Digite o novo CPF:");
  const novoTelefone = prompt("Digite o novo telefone:");

  if (!novoNome || !novaIdade || !novoCpf || !novoTelefone) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  const payload = {
    nome: novoNome,
    idade: parseInt(novaIdade),
    cpf: novoCpf,
    telefone: novoTelefone
  };

  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`Erro ao editar paciente: ${res.status}`);

    alert("✅ Paciente atualizado com sucesso!");
    carregarPacientes();
  } catch (err) {
    console.error(err);
    alert("❌ Erro ao editar paciente.");
  }
}


// =============== EXCLUIR PACIENTE (DELETE) ===============
async function excluirPaciente(id) {
  if (!confirm("Deseja realmente excluir este paciente?")) return;

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Erro ao excluir paciente");

    carregarPacientes();
  } catch (error) {
    console.error("❌ Erro ao excluir paciente:", error);
    alert("Erro ao excluir paciente!");
  }
}

// Inicializa a listagem ao carregar a página
carregarPacientes();
