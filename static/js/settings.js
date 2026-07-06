document.querySelectorAll(".model-option").forEach((option) => {
    option.addEventListener("click", () => {
        document.querySelectorAll(".model-option").forEach((o) => o.classList.remove("selected"));
        option.classList.add("selected");
        option.querySelector("input").checked = true;
    });
});
