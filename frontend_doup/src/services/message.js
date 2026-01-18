// invalid → dispara quando o campo obrigatório está vazio ou inválido e mostra sua mensagem personalizada.
// mensagem → dispara quando o usuário digita algo e limpa a mensagem personalizada para não ficar presa.

document.addEventListener("DOMContentLoaded", function () {
  montaTabela();
});

let tarefas = [];

function limpaCampos() {
  document.querySelector("#taskTitle").value = "";
  document.querySelector("#taskDescription").value = "";
}

function adicionaTarefa() {
  const titleInput = document.querySelector("#taskTitle");
  const title = titleInput.value;
  const description = document.querySelector("#taskDescription").value;

  // Verificar se o título está vazio e mostrar a mensagem de erro
  if (!titleInput.value) {
    titleInput.setCustomValidity("Campo título é obrigatório");
    titleInput.reportValidity(); // Exibe a mensagem de erro customizada
    return;
  } else {
    titleInput.setCustomValidity(""); // Remove a mensagem de erro quando o campo for válido
  }

  const existeTarefa = tarefas.find((tarefa) => tarefa.title === title);

  if (existeTarefa) {
    alert("Já existe uma tarefa com esse título");
    return;
  }

  tarefas.push({ title, description });

  montaTabela();

  limpaCampos();
}

function montaTabela() {
  const tabela = document.querySelector("#tabela");

  let html = `
  <table>
    <tr>
        <th>Título</th>
        <th>Descrição</th>
    </tr>
  `;

  tarefas.forEach((tarefa) => {
    html += `
            <tr>
                <td>${tarefa.title}</td>
                <td>${tarefa.description}</td>
            </tr>
            `;
  });

  html += "</table>";

  tabela.innerHTML = html;
}
