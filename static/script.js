async function atualizarStats(id, novaVida, novaMana) {
  try {
    const response = await fetch(`/atualizar_stats/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ vida: novaVida, mana: novaMana })
    });

    if (!response.ok) {
      throw new Error('Erro ao atualizar as estatísticas');
    }

    const data = await response.json();
    // Atualiza o HTML do card específico
    document.getElementById(`vida-${id}`).textContent = data.vida;
    document.getElementById(`mana-${id}`).textContent = data.mana;
    document.getElementById(`nome-${id}`).textContent = data.nome;
  } catch (error) {
    console.error('Erro ao atualizar as estatísticas:', error);
  }
}



let cards = document.querySelector('.card-container');

// Chamar a API para obter a lista de personagens
fetch('http://192.168.4.132:5001/personagem')
    .then(resposta => {
        if (!resposta.ok) {
            throw new Error('Erro ao carregar os dados');
        }
        return resposta.json();
    })
    .then(personagens => {
        // Iterar sobre os personagens e criar os cards
        personagens.forEach((personagem, indice) => {
            // Criar um card padrão
            let card = document.createElement('div');
            card.classList.add('card');

            // Preencher os dados de cada personagem
            card.innerHTML = `
                <h3>º ${indice + 1}</h3>
                <h2 id="nome-${indice}">${personagem.nome}</h2>
                <div class="stats">
                    <img id="outfit-${indice}" src="https://mythica.eu/outfits/animoutfit.php?id=${personagem.outType}&addons=3&head=${personagem.outHead}&body=${personagem.outBody}&legs=${personagem.outLegs}&feet=${personagem.outFeet}&mount=0&direction=3" alt="">
                    <p>Vida: <span class="life" id="vida-${indice}">${personagem.vida} %</span></p>
                    <p>Mana: <span class="mana" id="mana-${indice}">${personagem.mana} %</span></p>
                    <p>level: <span id="level-${indice}">${personagem.level}</span></p>
                    <p>Dinheiro: <span id="dinheiro-${indice}">${personagem.dinheiro} Cristal Coins</span></p>
                    <p>Potions: <span id="pot-${indice}">${personagem.pot}</span></p>
                    <p>Status: <span id="status-${indice}">${personagem.status}</span></p>
                    <input type="text" id="link" value="http://127.0.0.1:5001/atualizar_stats/${indice + 1}">
                </div>
            `;
            const potValue = personagem.pot;
            const manaValue = personagem.mana;
            const lifeValue = personagem.vida;


            if (potValue < 200 || manaValue < 20 || lifeValue < 20) {
                card.id = 'low-potions'; // Adiciona um ID único
            }

            // Colocar cada card dentro da div cards
            cards.appendChild(card);
            // Colocar cada card dentro da div cards
            cards.appendChild(card);
        });
    })
    .catch(error => {
        console.error('Erro ao buscar os dados:', error);
    });




document.getElementById('copiar').addEventListener('click', execCopy);
function execCopy() {
    document.querySelector("#link").select();
    document.execCommand("copy");
}


