function updateTotal() {
    let total = 0;
    document.querySelectorAll("#tasklist li").forEach(cb => {
        total += Number(cb.dataset.points);
    });
    document.getElementById("total").textContent = total;
}

window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".task-checkbox").forEach(cb => {
        cb.addEventListener("change", updateTotal);
    });
    updateTotal();
});
