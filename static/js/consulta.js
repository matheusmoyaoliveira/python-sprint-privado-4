// ================= CONSULTAS =================
const API_URL = "https://python-sprint-privado-4.onrender.com/api/consultas";

const form = document.getElementById("formConsulta");
const container = document.getElementById("listaConsultas");

// ================== CARREGAR CONSULTAS (GET) ==================
async function carregarConsultas() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Erro ${res.status}`);

    const consultas = await res.json();
    container.innerHTML = "";

    if (consultas.length === 0) {
      container.innerHTML = `<p style="text-align:center;">Nenhuma consulta agendada.</p>`;
      return;
    }

    consultas.forEach((c) => {
      const card = document.createElement("div");
      card.classList.add("card-consulta");

      card.innerHTML = `
        <div class="card-header">
          <h3>Consulta #${c.id}</h3>
        </div>
        <div class="card-body">
          <p><strong>Data/Hora:</strong> ${c.dataHora}</p>
          <p><strong>Modalidade:</strong> ${c.modalidade}</p>
          <p><strong>ID Paciente:</strong> ${c.idPaciente}</p>
          <p><strong>ID Médico:</strong> ${c.idMedico}</p>
        </div>
        <div class="card-footer">
          <button class="btn-delete" onclick="excluirConsulta(${c.id})">Excluir</button>
          <button class="btn-edit" onclick="editarConsulta(${c.id})">Editar</button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error("❌ Erro ao carregar consultas:", err);
    container.innerHTML = `<p style="color:red; text-align:center;">Erro ao carregar consultas.</p>`;
  }
}

// ================== ADICIONAR CONSULTA (POST) ==================
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const dataHora = document.getElementById("dataHora").value;
  const modalidade = document.getElementById("modalidade").value;
  const idPaciente = parseInt(document.getElementById("idPaciente").value);
  const idMedico = parseInt(document.getElementById("idMedico").value);

  if (!dataHora || !modalidade || !idPaciente || !idMedico) {
    alert("Preencha todos os campos!");
    return;
  }

  const novaConsulta = {
    dataHora,
    modalidade,
    idPaciente,
    idMedico
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(novaConsulta),
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("✅ Consulta agendada com sucesso!");
    form.reset();
    carregarConsultas();
  } catch (err) {
    console.error("❌ Erro ao agendar consulta:", err);
    alert("Erro ao agendar consulta.");
  }
});

// ================== EDITAR CONSULTA (PUT) ==================
async function editarConsulta(id) {
  const novaData = prompt("Digite a nova data/hora (yyyy-MM-dd HH:mm:ss):");
  const novaModalidade = prompt("Digite a nova modalidade (Presencial ou Online):");

  if (!novaData || !novaModalidade) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  const payload = {
    dataHora: novaData,
    modalidade: novaModalidade,
  };

  try {
    const res = await fetch(`${API_URL}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("✅ Consulta atualizada com sucesso!");
    carregarConsultas();
  } catch (err) {
    console.error("❌ Erro ao editar consulta:", err);
    alert("Erro ao editar consulta.");
  }
}

// ================== EXCLUIR CONSULTA (DELETE) ==================
async function excluirConsulta(id) {
  if (!confirm("Tem certeza que deseja excluir esta consulta?")) return;

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`Erro ${res.status}`);

    alert("🗑️ Consulta excluída com sucesso!");
    carregarConsultas();
  } catch (err) {
    console.error("❌ Erro ao excluir consulta:", err);
    alert("Erro ao excluir consulta.");
  }
}

// ================== INICIALIZA ==================
carregarConsultas();
