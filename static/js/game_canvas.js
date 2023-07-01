(() => {
  window.addEventListener("load", () => {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("load", function (event) {
      let res = JSON.parse(event.target.responseText);
      initGame(res);

      if (res["player"] !== "X") {
        setTimeout(() => {
          IA();
        }, 500);
      }
    });

    xhr.open("GET", `http://127.0.0.1:5000/play`);

    xhr.send(null);
  });

  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  let board = null;
  let currentPlayer = null;
  let winner = null;

  const initGame = (res) => {
    currentPlayer = "X";
    board = res["board"];

    if (res["player"] === "X") {
      document.querySelector(".cross").innerHTML = "You";
      document.querySelector(".circle").innerHTML = "IA";
    } else {
      document.querySelector(".cross").innerHTML = "IA";
      document.querySelector(".circle").innerHTML = "You";
    }
    document.querySelector(".difficulty").innerHTML = res["difficulty"];
    document.querySelector(".round").innerHTML = currentPlayer;

    drawBoard();
  };

  const cellSize = 100;
  const gridSize = 3;
  canvas.width = cellSize * gridSize;
  canvas.height = cellSize * gridSize;

  const drawBoard = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        const cellX = col * cellSize;
        const cellY = row * cellSize;
        const cellValue = board[row][col];

        ctx.fillStyle = "lightgray";
        ctx.fillRect(cellX, cellY, cellSize, cellSize);

        ctx.strokeStyle = "black";
        ctx.strokeRect(cellX, cellY, cellSize, cellSize);

        ctx.font = "bold 48px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        if (cellValue !== "") {
          ctx.fillStyle = "black";
          ctx.fillText(cellValue, cellX + cellSize / 2, cellY + cellSize / 2);
        }
      }
    }
  };

  canvas.addEventListener("click", (event) => {
    if (!winner) {
      const rect = canvas.getBoundingClientRect();
      const offsetX = event.clientX - rect.left;
      const offsetY = event.clientY - rect.top;
      const col = Math.floor(offsetX / cellSize);
      const row = Math.floor(offsetY / cellSize);

      if (board[row][col] === "") {
        sendCoord(row, col);
      }
    }
  });

  const sendCoord = (row, col) => {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("load", function (event) {
      let res = JSON.parse(event.target.responseText);
      board = res["board"];
      drawBoard();

      winner = res["winner"];
      if (winner) {
        setTimeout(() => {
          alert(`Player ${currentPlayer} wins !`);
        }, 250);
      } else if (res["board_full"]) {
        setTimeout(() => {
          alert("Match nul !");
        }, 250);
      } else {
        currentPlayer = res["current_player"];
        document.querySelector(".round").innerHTML = currentPlayer;

        setTimeout(() => {
          IA();
        }, 500);
      }
    });

    xhr.open(
      "GET",
      `http://127.0.0.1:5000/process?row=${row}&&col=${col}&&current_player=${currentPlayer}`
    );

    xhr.send(null);
  };

  const IA = () => {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("load", function (event) {
      let res = JSON.parse(event.target.responseText);
      board = res["board"];
      drawBoard();

      winner = res["winner"];
      if (winner) {
        setTimeout(() => {
          alert(`Player ${currentPlayer} wins !`);
        }, 250);
      } else if (res["board_full"]) {
        setTimeout(() => {
          alert("Match nul !");
        }, 250);
      } else {
        currentPlayer = res["current_player"];
        document.querySelector(".round").innerHTML = currentPlayer;
      }
    });

    xhr.open(
      "GET",
      `http://127.0.0.1:5000/process?current_player=${currentPlayer}`
    );

    xhr.send(null);
  };
})();
