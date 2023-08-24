/**
 * start: An indicator wheater the prerequesities are fulfilled to starte
 * the game.
 * requiredGift: Gift required to enter the raffle.
 * minGiftAmount: Minimum gift amount required ot enter the game.
 * minGiftAmountToStart:
 * minParticipantToStart:
 */
const gameInfo = {
  start: false,
  requiredGift: "rose",
  minGiftAmount: 5,
  minGiftToStart: 300,
  minParticipant: 9,
  totalAmount: 0,
  totalParticipants: 0,
  lastWinner: "No Winner Yet",
  delay: false,
  winner_delay: false
}

/* Websocket connection */
const websocket = new WebSocket("ws://localhost:8001");


/* HTML Elements */
const input_account_id = document.querySelector("#unique-id")
const start = document.querySelector("#start");

/* counter */
let counter;

function sleep (ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * count - counts down from 10 1.
 *
 */
async function count() {
  const starter = document.querySelector(".starter");
  const starterCounter = document.querySelector(".starter-counter");
      
  if (!(counter) && String(counter) !== '0') {
    counter = 10;
  } else if (counter < 0) {
    counter = undefined;
    starter.style.display = "none";
    await sleep(1000);
    return;
  }
  starter.style.display = "flex";

  starterCounter.textContent = String(counter);
  counter--;
  setTimeout(count, 1000);
}

async function displayMessage (type, message) {
  const messageContainer = document.querySelector(".message");
  
  if (type == "error") {
    messageContainer.style.background = "#FF0000A0";
  } else if (type == "warning") {
    messageContainer.style.background = "#0000FFA0";
  }
  messageContainer.textContent = message;
  messageContainer.style.display = "block";
  await sleep(10000);
  messageContainer.style.display = "none";
}

function initGame () {
  const idPrompot = document.querySelector(".get-initialization-info");
  const gameContainer = document.querySelector(".container");

  /* VALUES */
  const lastWinner = document.querySelector("#last-winner");
  const requiredGift = document.querySelector("#required-gift-type");
  const minParticipant = document.querySelector("#min-participant");
  const minGiftAmount = document.querySelector("#required-gift-amount");
  const totalAmount = document.querySelector("#total-amount");
  const totalParticipants = document.querySelector("#total-participants");


  lastWinner.textContent = gameInfo.lastWinner;
  requiredGift.textContent = gameInfo.requiredGift;
  minGiftAmount.textContent = gameInfo.minGiftAmount;
  minParticipant.textContent = gameInfo.minParticipant + " %";
  totalAmount.textContent = gameInfo.totalAmount
  totalParticipants.textContent = gameInfo.totalParticipants;

  idPrompot.style.display = "none";
  gameContainer.style.display = "block";
}


async function reflectUpdate () {
  const notifications = document.querySelector(".notifications");
  const lastWinner = document.querySelector("#last-winner");
  const requiredGift = document.querySelector("#required-gift-type");
  const minGiftAmount = document.querySelector("#required-gift-amount");
  const totalAmount = document.querySelector("#total-amount");
  const totalParticipants = document.querySelector("#total-participants");

  lastWinner.textContent = gameInfo.lastWinner;
  requiredGift.textContent = gameInfo.requiredGift;
  minGiftAmount.textContent = gameInfo.minGiftAmount;
  totalAmount.textContent = gameInfo.totalAmount;
  totalParticipants.textContent = gameInfo.totalParticipants;

  const newParticipants = gaminfo.newParticipants.slice()
  if (!gameInfo.winner_delay) {
    notifications.style.display = "block";
    if (gameInfo.delay) {
      await sleep(5000 * gameInfo.delay);
    }
  }

  gameInfo.delay = newParticipants.length;
  
  for (let i = 0; i < newParticipants.length && !(gameInfo.winner_delay); i++) {
    notifications.textContent = newParticipants[i] + " joined the raffle";
    await sleep(5000);
  }
  notifications.style.display = "none";
  
  if (gameinfo.stop === true) {
    displayMessage("warning", "Live stream has ended")
    websocket.close(1000)
  } else  if (gameInfo.go === true) {
    gameInfo.go = false;
    const opdata = {
      type: "start",
      body: {}
    }
    websocket.send(JSON.stringify(opdata));
  }
}


async function announceWinner(winner_id) {
  gameInfo.winner_delay = true;
  const notifications = document.querySelector(".notifications");
  notifications.style.display = "none";
  const winner = document.querySelector(".winner");
  const raffleStatus = document.querySelector(".raffle-status");
  await count();
  raffleStatus.textContent = "COUNTDOWN";
  await sleep(10000);
  raffleStatus.textContent = "WINNER";
  winner.textContent = winner_id;
  winner.style.display = "block";
  await sleep(20000);
  winner.style.display = "none";
  raffleStatus.textContent = "WAITING";
  gameInfo.winner_delay = false;
}

start.addEventListener ("click", () => {
  const re = /^@[a-zA-Z0-9_\.]+[a-zA-Z0-9_]$/g;
  if (re.test(input_account_id.value)) {
    console.log("Init message sent");
    gameInfo.uniqueId = input_account_id.value;
    let opdata = {
      type: "init",
      body: {
          uniqueId: gameInfo.uniqueId
      }
    }
    opdata = JSON.stringify(opdata);
    websocket.send(opdata)
  } else {
    displayMessage("warning", "Invalid User name please enter a valid user name")
  }
});


websocket.addEventListener("message", ({data}) => {
  console.log(data);
  data = JSON.parse(data);
  console.log(data);
  const type = data["type"];
  const body = data["body"];
  let keys;
  console.log("body :", body, "\n", "data.body: ", data.body)
  switch (type) {
    case "error":
      displayMessage("error", body.message)
      break;
    case "success":
      keys = Object.entries(body);
      console.log(keys);
      for (let i = 0; i < keys.length; i++) {
        console.log("key: ", keys[i][0], "\nValue:", body[keys[i][0]]);
        gameInfo[keys[i][0]] = body[keys[i][0]];
      }
      initGame()
      break;
    case "update":
      keys = Object.entries(body);
      console.log(keys);
      for (let i = 0; i < keys.length; i++) {
        console.log("key: ", keys[i][0], "\nValue:", body[keys[i][0]]);
        gameInfo[keys[i][0]] = body[keys[i][0]];
      }
      reflectUpdate();
      break;
    case "winner":
      announceWinner(body.winner);
      break;
  }
});
