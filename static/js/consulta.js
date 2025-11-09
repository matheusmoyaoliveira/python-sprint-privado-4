// ================= CONSULTAS =================
const API_URL = "https://python-sprint-privado-4.onrender.com/api/consultas";
const form = document.getElementById("formConsulta");
const container = document.getElementById("listaConsultas");

// ================== FORMATAÇÃO DE DATA ==================
function formatarData(dataISO) {
  try {
    const data = new Date(dataISO);
    const dia = String(data.getDate()).padStart(2, "0");
    const mes = String(data.getMonth() + 1).padStart(2, "0");
    const ano = data.getFullYear();
    const hora = String(data.getHours()).padStart(2, "0");
    const min = String(data.getMinutes()).padStart(2, "0");
    return `${dia}/${mes}/${ano} ${hora}:${min}`;
  } catch {
    return dataISO;
  }
}

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
          <p><strong>Data/Hora:</strong> ${formatarData(c.dataHora)}</p>
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

  const data = document.getElementById("data").value;
  const hora = document.getElementById("hora").value;
  const modalidade = document.getElementById("modalidade").value;
  const idPaciente = parseInt(document.getElementById("idPaciente").value);
  const idMedico = parseInt(document.getElementById("idMedico").value);

  if (!data || !hora || !modalidade || !idPaciente || !idMedico) {
    alert("Preencha todos os campos!");
    return;
  }

  // Junta data + hora no formato esperado pela API
  const dataHora = `${data} ${hora}:00`;
  const novaConsulta = { dataHora, modalidade, idPaciente, idMedico };

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
  const novaData = prompt("Digite a nova data (AAAA-MM-DD):");
  const novaHora = prompt("Digite a nova hora (HH:MM):");
  const novaModalidade = prompt("Digite a nova modalidade (Presencial ou Online):");

  if (!novaData || !novaHora || !novaModalidade) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  const novaDataHora = `${novaData} ${novaHora}:00`;
  const payload = { dataHora: novaDataHora, modalidade: novaModalidade };

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
