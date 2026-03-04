const lvlText = document.querySelector("#level");
const hpText = document.querySelector("#health");
const maxHpText = document.querySelector("#max-health");
const nameText = document.querySelector("#name");
const knightImage = document.querySelector("#knight_gif");
const atkBtn = document.querySelector("#attack-btn");
const levelBtn = document.querySelector("#levelup-btn");
const page = document.body;

let deadYet = false;

const character = {
  name: "Knight",
  class: "Human Soldier",
  level: Number(lvlText.textContent),
  health: Number(hpText.textContent),
  image: "images/knight.gif",

  attacked() {
    this.health = Math.max(0, this.health - 20);
  },

  levelUp() {
    this.level += 1;
  }
};

function updateStats() {
  nameText.textContent = character.name;
  knightImage.setAttribute("src", character.image);
  lvlText.textContent = character.level;
  hpText.textContent = character.health;
  maxHpText.textContent = Number(maxHpText.textContent);
}

function showYouDied() {
  if (deadYet) {
    return;
  }

  deadYet = true;
  atkBtn.disabled = true;
  levelBtn.disabled = true;
  page.classList.add("dead");
}

// I'm making a game for another class so I'm all about those random numbers

atkBtn.addEventListener("click", () => {
  if (deadYet) {
    return;
  }

  character.attacked();
  updateStats();

  if (character.health <= 0) {
    showYouDied();
  }
});

levelBtn.addEventListener("click", () => {
  if (deadYet) {
    return;
  }

  character.levelUp();
  updateStats();
});

updateStats();
