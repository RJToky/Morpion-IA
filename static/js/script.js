const setting = document.querySelector(".setting");
const modal = document.querySelector(".modal");
setting.addEventListener("click", () => {
  modal.classList.toggle("active");
});

const bg = document.querySelector(".modal .bg");
bg.addEventListener("click", () => {
  modal.classList.toggle("active");
});
